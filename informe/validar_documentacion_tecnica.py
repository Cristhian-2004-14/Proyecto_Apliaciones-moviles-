from pathlib import Path

from docx import Document


root = Path(__file__).resolve().parent.parent / 'documentación técnica'
for path in sorted(root.glob('*.docx')):
    document = Document(path)
    print(
        f'{path.name}: párrafos={len(document.paragraphs)}, '
        f'tablas={len(document.tables)}, título={document.paragraphs[0].text}'
    )
for path in sorted(root.glob('*.md')):
    print(f'{path.name}: líneas={len(path.read_text(encoding="utf-8").splitlines())}')
