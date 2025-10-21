# Image Transform Tool

Piccolo tool da riga di comando per trasformare immagini con effetti artistici di stampa.

## Caratteristiche

- **Halftone a punti**: Effetto retinatura tipo stampa newsprint/risograph con punti circolari
- **Dithering 1-bit**: Dithering con matrice Bayer 8×8 per immagini in bianco e nero
- **Posterizzazione 2-toni**: Effetto stencil/pochoir con solo due toni

## Installazione

```bash
pip install -r requirements.txt
chmod +x imgtransform.py
```

## Utilizzo

### Sintassi base

```bash
python imgtransform.py -i INPUT -o OUTPUT [MODE] [OPTIONS]
```

### Modalità

#### 1. Halftone (Retinatura a punti)

Crea un effetto di stampa a punti tipico delle stampe newsprint o risograph:

```bash
python imgtransform.py -i input.jpg -o output.png --halftone
```

**Opzioni:**
- `--dot-size N`: Dimensione dei punti in pixel (default: 8)
- `--scale N`: Fattore di scala dell'output (default: 1)

**Esempi:**
```bash
# Punti più grandi
python imgtransform.py -i foto.jpg -o halftone.png --halftone --dot-size 12

# Punti piccoli con output ingrandito
python imgtransform.py -i foto.jpg -o halftone_hires.png --halftone --dot-size 6 --scale 2
```

#### 2. Dithering Bayer 8×8

Applica dithering 1-bit con matrice Bayer 8×8 per un effetto di stampa classica:

```bash
python imgtransform.py -i input.jpg -o output.png --dither
```

Ottimo per:
- Effetti retrò computer grafica
- Stampe su carta
- Riduzioni a 1-bit mantenendo dettagli

#### 3. Posterizzazione 2-toni

Crea immagini con solo due toni (bianco e nero) perfette per stencil o pochoir:

```bash
python imgtransform.py -i input.jpg -o output.png --posterize
```

**Opzioni:**
- `--threshold N`: Soglia di separazione tra nero e bianco, 0-255 (default: 128)

**Esempi:**
```bash
# Più nero (soglia alta)
python imgtransform.py -i foto.jpg -o stencil_dark.png --posterize --threshold 180

# Più bianco (soglia bassa)
python imgtransform.py -i foto.jpg -o stencil_light.png --posterize --threshold 80
```

## Esempi completi

```bash
# Halftone per poster retrò
python imgtransform.py -i portrait.jpg -o poster.png --halftone --dot-size 10

# Dithering per estetica pixel art
python imgtransform.py -i landscape.jpg -o retro.png --dither

# Stencil per serigrafia
python imgtransform.py -i logo.png -o stencil.png --posterize --threshold 140
```

## Formati supportati

- **Input**: JPG, PNG, BMP, GIF, TIFF, WebP (tutti i formati PIL)
- **Output**: Qualsiasi formato supportato da PIL (raccomandato PNG per qualità)

## Suggerimenti

1. **Halftone**: Usa `--scale 2` o superiore per output ad alta risoluzione
2. **Dithering**: Funziona meglio con immagini che hanno buon contrasto
3. **Posterizzazione**: Sperimenta con valori di threshold tra 100-150 per risultati ottimali
4. Per stampe, salva in PNG per preservare i dettagli

## Requisiti

- Python 3.7+
- Pillow (PIL)
- NumPy

## Licenza

MIT
