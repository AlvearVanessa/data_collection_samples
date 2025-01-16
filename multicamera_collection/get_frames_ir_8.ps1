# Define la ruta del directorio que contiene los archivos
$sourceFolder = "D:\FondoBiblioteca\VideosFemto_IR" 

# Obtiene una lista de archivos en el directorio especificado
$fileFolder = Get-ChildItem -Path $sourceFolder -File
 
# Itera sobre cada archivo en la carpeta de origen
foreach ($file in $fileFolder) {
    
    # Comprueba si el archivo existe usando la ruta completa
    if (Test-Path -Path $file.FullName) {
        # Extrae el nombre del archivo sin la extensión para crear un nuevo directorio
        $fileNameWithoutExtension = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $newDir = Join-Path -Path $sourceFolder -ChildPath $fileNameWithoutExtension
 
        # Crea el nuevo directorio si no existe
        if (-Not (Test-Path -Path $newDir)) {
            mkdir -Path $newDir | Out-Null
            cd $newDir
            ffmpeg -i $file.FullName -map 0:2 -vsync 0 ir%03d.png
        }
 
        # Mueve el archivo al nuevo directorio
        $destination = Join-Path -Path $newDir -ChildPath $file.Name
        Move-Item -Path $file.FullName -Destination $destination

    }
}

