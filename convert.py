"""Convierte PDFs de la carpeta "Certificaciones" a imágenes PNG.

Uso:
  python convert.py
  python convert.py --input "Certificaciones" --output "Certificaciones en imágenes png" --dpi 200

Requiere: PyMuPDF (`pip install -r requirements.txt`)
"""

from pathlib import Path
import argparse
import fitz  # PyMuPDF


def convert_pdf_to_png(input_dir: Path, output_dir: Path, dpi: int = 150):
	input_dir = Path(input_dir)
	output_dir = Path(output_dir)
	output_dir.mkdir(parents=True, exist_ok=True)

	pdf_files = sorted(input_dir.glob("*.pdf"))
	if not pdf_files:
		print(f"No se encontraron archivos PDF en: {input_dir}")
		return

	for pdf_path in pdf_files:
		doc = fitz.open(pdf_path)
		stem = pdf_path.stem
		for page_index in range(len(doc)):
			page = doc[page_index]
			# Escala para DPI deseado (72 DPI es referencia de fitz)
			zoom = dpi / 72
			mat = fitz.Matrix(zoom, zoom)
			pix = page.get_pixmap(matrix=mat, alpha=False)
			out_name = f"{stem}_page{page_index+1:03d}.png"
			out_path = output_dir / out_name
			pix.save(str(out_path))
			print(f"Guardado: {out_path}")
		doc.close()


def main():
	parser = argparse.ArgumentParser(description="Convertir PDFs a PNG por página")
	parser.add_argument("--input", "-i", default="Certificaciones", help="Carpeta con archivos PDF")
	parser.add_argument("--output", "-o", default="Certificaciones en imágenes png", help="Carpeta de salida para PNG")
	parser.add_argument("--dpi", type=int, default=150, help="Resolución en DPI para las imágenes (mayor = mejor calidad)")
	args = parser.parse_args()

	input_dir = Path(args.input)
	output_dir = Path(args.output)

	if not input_dir.exists() or not input_dir.is_dir():
		print(f"La carpeta de entrada no existe: {input_dir}")
		return

	convert_pdf_to_png(input_dir, output_dir, dpi=args.dpi)


if __name__ == "__main__":
	main()

