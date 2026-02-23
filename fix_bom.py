import sys

with open(sys.argv[1], 'rb') as f:
    content = f.read()

# Eliminar la BOM UTF-8 si existeix (bytes \xef\xbb\xbf)
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]
    print("BOM eliminada correctament.")
else:
    print("No s'ha trobat BOM, el fitxer ja és net.")

with open(sys.argv[1], 'wb') as f:
    f.write(content)