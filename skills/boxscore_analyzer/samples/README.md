Place sample boxscore images here for manual testing and CI-friendly datasets.

The test suite will run an end-to-end OCR->parse->stats integration test when
sample images are present. For automated CI, it's recommended to monkeypatch
`pytesseract.image_to_string` (the included tests already do this).

Add images like:

- `game1.jpg`
- `game2.png`

To use real images in tests, add them to this directory and the integration
test will detect and run against them.
