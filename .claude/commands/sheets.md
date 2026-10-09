Generate badge sheets for a show by running generate_sheets.py.

Usage: /sheets shows/2026_The_Sound_of_Music
       /sheets shows/2026_The_Sound_of_Music --no-pdf

Run the following command and report what was produced:

```bash
python3 generate_sheets.py $ARGUMENTS/config.yaml
```

If the command fails, diagnose the error and suggest a fix. Common issues:
- Missing config.yaml: offer to create one from the template
- Missing art files: check that front_art and back_art paths in config.yaml are correct relative to the show directory
- Missing names CSV: check the names_csv path in config.yaml
- PDF conversion fails: suggest running with --no-pdf and installing librsvg2-bin
