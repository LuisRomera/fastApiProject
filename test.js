/**
 * Guarda un array 2D masivo en Drive, particionado y comprimido.
 * Requiere el Servicio Avanzado de Drive API v3.
 */
function guardarFicherosGigantes(folderId, prefijo, datos2D, tamañoParticionFilas = 50000) {
  const lock = LockService.getScriptLock();
  
  // Esperamos hasta 30 segundos por si otro proceso está escribiendo
  if (!lock.tryLock(30000)) {
    throw new Error("El sistema está ocupado guardando otros datos. Inténtalo de nuevo.");
  }

  try {
    // Generamos un timestamp único (ej: 20260325_153022)
    const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyyMMdd_HHmmss");
    let numeroParticion = 1;

    // Bucle para particionar el array 2D
    for (let i = 0; i < datos2D.length; i += tamañoParticionFilas) {
      // 1. Extraer el bloque (chunk) de datos
      const chunk = datos2D.slice(i, i + tamañoParticionFilas);
      
      // 2. Convertir a String JSON
      const jsonStr = JSON.stringify(chunk);
      
      // 3. Crear Blob y Comprimir a GZIP (Vital para rendimiento)
      const blob = Utilities.newBlob(jsonStr, 'application/json', 'temp.json');
      const gzipBlob = Utilities.gzip(blob);
      
      // 4. Metadatos para Drive v3
      const nombreFichero = `${prefijo}_${timestamp}_part${numeroParticion}.gz`;
      const resource = {
        name: nombreFichero,
        parents: [folderId],
        mimeType: 'application/gzip'
      };

      // 5. Guardar usando Drive v3
      Drive.Files.create(resource, gzipBlob);
      
      console.log(`Guardado: ${nombreFichero}`);
      numeroParticion++;
    }
    
    return true; // Éxito
    
  } catch (e) {
    console.error("Error al guardar: " + e.toString());
    throw e;
  } finally {
    lock.releaseLock(); // Siempre liberar el candado
  }
}


/**
 * Lee y reconstruye los últimos ficheros guardados con un prefijo específico.
 * Requiere el Servicio Avanzado de Drive API v3.
 */
function leerUltimosFicheros(folderId, prefijo) {
  // 1. Buscar ficheros con ese prefijo ordenados por fecha de creación (los más nuevos primero)
  // Nota: en Drive v3 se usa 'files' en lugar de 'items'
  const query = `'${folderId}' in parents and name contains '${prefijo}_' and trashed = false`;
  const listaV3 = Drive.Files.list({
    q: query,
    orderBy: 'createdTime desc',
    fields: 'files(id, name, createdTime)'
  }).files;

  if (!listaV3 || listaV3.length === 0) {
    return []; // No hay datos
  }

  // 2. Identificar el "timestamp" del fichero más reciente
  // El nombre tiene formato: prefijo_timestamp_partX.gz
  const nombreMasReciente = listaV3[0].name;
  const match = nombreMasReciente.match(new RegExp(`${prefijo}_(\\d{8}_\\d{6})_part`));
  
  if (!match) throw new Error("Formato de nombre de archivo no reconocido.");
  const ultimoTimestamp = match[1];

  // 3. Filtrar solo los ficheros que pertenezcan a ese exacto timestamp (las particiones)
  const ficherosDeEstaVersion = listaV3.filter(f => f.name.includes(ultimoTimestamp));
  
  // Ordenarlos por número de partición para reconstruir el array en el orden correcto
  ficherosDeEstaVersion.sort((a, b) => a.name.localeCompare(b.name));

  let datosCompletos = [];

  // 4. Leer, descomprimir y unir
  for (const fichero of ficherosDeEstaVersion) {
    console.log(`Leyendo partición: ${fichero.name}`);
    
    // Obtenemos el Blob comprimido usando DriveApp (es más fácil manejar blobs binarios aquí que con Drive.Files.get)
    const blobComprimido = DriveApp.getFileById(fichero.id).getBlob();
    
    // Descomprimimos GZIP al vuelo
    const blobDescomprimido = Utilities.ungzip(blobComprimido);
    
    // Pasamos a String y luego a JSON
    const jsonStr = blobDescomprimido.getDataAsString();
    const matrizParticion = JSON.parse(jsonStr);
    
    // Concatenamos al array principal (usar un bucle para evitar error de stack overflow en arrays gigantes con push(...))
    for(let fila of matrizParticion) {
       datosCompletos.push(fila);
    }
  }

  console.log(`Total de filas recuperadas: ${datosCompletos.length}`);
  return datosCompletos;
}
