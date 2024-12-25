DESTDIR ?= ./

TYPST_OPTS := --font-path $(TYPST_FONT_PATHS) --ignore-system-fonts
PREPROCESSOR = maint/preprocess.py
VERSCRIPT := maint/version.py

META_EN = maint/metadata.en.yml
META_RU = maint/metadata.ru.yml
STYLING_PDF = maint/styling.typst

CHAPTERS_EN += text/en/01-tumble.typ
CHAPTERS_EN += text/en/02-walk.typ
CHAPTERS_EN += text/en/03-drop.typ
CHAPTERS_EN += text/en/04-getaway.typ
CHAPTERS_EN += text/en/05-glide.typ
CHAPTERS_EN += text/en/06-rise.typ
CHAPTERS_EN += text/en/07-retreat.typ
CHAPTERS_EN += text/en/08-exit.typ

CHAPTERS_RU += text/ru/01-tumble.typ
CHAPTERS_RU += text/ru/02-walk.typ
CHAPTERS_RU += text/ru/03-drop.typ
CHAPTERS_RU += text/ru/04-getaway.typ
CHAPTERS_RU += text/ru/05-glide.typ
CHAPTERS_RU += text/ru/06-rise.typ
CHAPTERS_RU += text/ru/07-retreat.typ
CHAPTERS_RU += text/ru/08-exit.typ

VERFILE := $(DESTDIR)/.version

.PHONY: outputs
outputs: $(DESTDIR)/in-maxines-way.en-ru.pdf
outputs: $(DESTDIR)/in-maxines-way.en.pdf
outputs: $(DESTDIR)/in-maxines-way.ru.pdf
outputs: $(DESTDIR)/in-maxines-way.en.epub
outputs: $(DESTDIR)/in-maxines-way.ru.epub
outputs: $(DESTDIR)/in-maxines-way.en.fb2
outputs: $(DESTDIR)/in-maxines-way.ru.fb2
outputs: $(DESTDIR)/in-maxines-way.en.80column.txt
outputs: $(DESTDIR)/in-maxines-way.ru.80column.txt
outputs: $(DESTDIR)/in-maxines-way.en.freeflow.txt
outputs: $(DESTDIR)/in-maxines-way.ru.freeflow.txt
all: outputs
clean:
	rm -f $(DESTDIR)/.version
	rm -f $(DESTDIR)/in-maxines-way.en-ru.pdf
	rm -f $(DESTDIR)/in-maxines-way.en.align.pdf in-maxines-way.ru.align.pdf
	rm -f $(DESTDIR)/in-maxines-way.ru.pdf.typ $(DESTDIR)/in-maxines-way.ru.pdf
	rm -f $(DESTDIR)/in-maxines-way.en.pdf.typ $(DESTDIR)/in-maxines-way.en.pdf
	rm -f $(DESTDIR)/in-maxines-way.en.epub.typ
	rm -f $(DESTDIR)/in-maxines-way.en.epub
	rm -f $(DESTDIR)/in-maxines-way.ru.epub.typ
	rm -f $(DESTDIR)/in-maxines-way.ru.epub
	rm -f $(DESTDIR)/in-maxines-way.en.fb2.typ $(DESTDIR)/in-maxines-way.en.fb2
	rm -f $(DESTDIR)/in-maxines-way.ru.fb2.typ $(DESTDIR)/in-maxines-way.ru.fb2
	rm -f $(DESTDIR)/in-maxines-way.en.80column.txt
	rm -f $(DESTDIR)/in-maxines-way.ru.80column.txt
	rm -f $(DESTDIR)/in-maxines-way.en.freeflow.txt
	rm -f $(DESTDIR)/in-maxines-way.ru.freeflow.txt
	rm -f $(DESTDIR)/.check-lt-en $(DESTDIR)/.check-lt-ru
	rm -f $(DESTDIR)/.check-wc

$(DESTDIR):
	mkdir -p $(DESTDIR)

$(VERFILE): $(VERSCRIPT) $(DESTDIR) $(PREPROCESSOR) $(STYLING_PDF)
$(VERFILE): $(META_EN) $(CHAPTERS_EN)
$(VERFILE): $(META_RU) $(CHAPTERS_RU)
	$(VERSCRIPT) -u $@

# PDF

$(DESTDIR)/in-maxines-way.en.pdf.typ: $(PREPROCESSOR) $(VERFILE) $(STYLING_PDF)
$(DESTDIR)/in-maxines-way.en.pdf.typ: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format pdf \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		--process-template $(STYLING_PDF) \
		$(CHAPTERS_EN) > $@
$(DESTDIR)/in-maxines-way.en.pdf: $(DESTDIR)/in-maxines-way.en.pdf.typ
	typst compile $(TYPST_OPTS) $< $@

$(DESTDIR)/in-maxines-way.ru.pdf.typ: $(PREPROCESSOR) $(VERFILE) $(STYLING_PDF)
$(DESTDIR)/in-maxines-way.ru.pdf.typ: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format pdf \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		--process-template $(STYLING_PDF) \
		$(CHAPTERS_RU) > $@
$(DESTDIR)/in-maxines-way.ru.pdf: $(DESTDIR)/in-maxines-way.ru.pdf.typ
	typst compile $(TYPST_OPTS) $< $@

# a 'debugging' PDF with all the languages

$(DESTDIR)/in-maxines-way.en.align.pdf.typ: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.en.align.pdf.typ: $(STYLING_PDF)
$(DESTDIR)/in-maxines-way.en.align.pdf.typ: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format pdf --align \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		--process-template $(STYLING_PDF) \
		$(CHAPTERS_EN) > $@
$(DESTDIR)/in-maxines-way.en.align.pdf: $(DESTDIR)/in-maxines-way.en.align.pdf.typ
	typst compile $(TYPST_OPTS) $< $@

$(DESTDIR)/in-maxines-way.ru.align.pdf.typ: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.ru.align.pdf.typ: $(STYLING_PDF)
$(DESTDIR)/in-maxines-way.ru.align.pdf.typ: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format pdf --align \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		--process-template $(STYLING_PDF) \
		$(CHAPTERS_RU) > $@
$(DESTDIR)/in-maxines-way.ru.align.pdf: $(DESTDIR)/in-maxines-way.ru.align.pdf.typ
	typst compile $(TYPST_OPTS) $< $@

$(DESTDIR)/in-maxines-way.en-ru.pdf: $(DESTDIR)/in-maxines-way.en.align.pdf
$(DESTDIR)/in-maxines-way.en-ru.pdf: $(DESTDIR)/in-maxines-way.ru.align.pdf
	cpdf \
	     -collate \
	     $(DESTDIR)/in-maxines-way.en.align.pdf \
	     $(DESTDIR)/in-maxines-way.ru.align.pdf \
	     AND \
	     -twoup-stack \
	     AND \
	     -rotate 90 \
	     -o $@

# EPUB

$(DESTDIR)/in-maxines-way.en.epub.typ: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.en.epub.typ: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format epub \
		--book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		$(CHAPTERS_EN) > $@
$(DESTDIR)/in-maxines-way.en.epub: $(DESTDIR)/in-maxines-way.en.epub.typ $(META_EN)
	pandoc --metadata-file $(META_EN) $< -o $@

$(DESTDIR)/in-maxines-way.ru.epub.typ: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.ru.epub.typ: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format epub \
		--book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		$(CHAPTERS_RU) > $@
$(DESTDIR)/in-maxines-way.ru.epub: $(DESTDIR)/in-maxines-way.ru.epub.typ $(META_RU)
	pandoc --metadata-file $(META_RU) $< -o $@

# FB2

$(DESTDIR)/in-maxines-way.en.fb2.typ: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.en.fb2.typ: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format fb2 \
		--book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		$(CHAPTERS_EN) > $@
$(DESTDIR)/in-maxines-way.en.fb2: $(DESTDIR)/in-maxines-way.en.fb2.typ $(META_EN)
	pandoc --metadata-file $(META_EN) $< -o $@

$(DESTDIR)/in-maxines-way.ru.fb2.typ: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.ru.fb2.typ: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format fb2 \
		--book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		$(CHAPTERS_RU) > $@
$(DESTDIR)/in-maxines-way.ru.fb2: $(DESTDIR)/in-maxines-way.ru.fb2.typ $(META_RU)
	pandoc --metadata-file $(META_RU) $< -o $@

# TXT

$(DESTDIR)/in-maxines-way.en.80column.txt: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.en.80column.txt: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format 80column.txt \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/in-maxines-way.ru.80column.txt: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.ru.80column.txt: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format 80column.txt \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		$(CHAPTERS_RU) > $@

$(DESTDIR)/in-maxines-way.en.freeflow.txt: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.en.freeflow.txt: $(META_EN) $(CHAPTERS_EN)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang en --format freeflow.txt \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_EN) \
		$(CHAPTERS_EN) > $@

$(DESTDIR)/in-maxines-way.ru.freeflow.txt: $(PREPROCESSOR) $(VERFILE)
$(DESTDIR)/in-maxines-way.ru.freeflow.txt: $(META_RU) $(CHAPTERS_RU)
	mkdir -p $(DESTDIR)
	$(PREPROCESSOR) --lang ru --format freeflow.txt \
	        --book-version v$(shell cat $(VERFILE)) \
		--process-meta $(META_RU) \
		$(CHAPTERS_RU) > $@

### checks

check: $(DESTDIR)/.check-lt-ru $(DESTDIR)/.check-lt-en
check: $(DESTDIR)/.check-wc
.PHONY: check
all: check

LTEX_EN += .ltex/ltex.dictionary.en-GB.txt
LTEX_EN += .ltex/ltex.disabledRules.en-GB.txt
LTEX_EN += .ltex/ltex.hiddenFalsePositives.en-GB.txt

LTEX_RU += .ltex/ltex.dictionary.ru-RU.txt
LTEX_RU += .ltex/ltex.disabledRules.ru-RU.txt
LTEX_RU += .ltex/ltex.hiddenFalsePositives.ru-RU.txt

CHECK_LANGUAGETOOL := maint/languagetool.py
CHECK_WC := maint/wc.py

$(DESTDIR)/.check-lt-en: $(CHECK_LANGUAGETOOL) $(LTEX_EN) $(CHAPTERS_EN)
	$(CHECK_LANGUAGETOOL) --lang en-GB --unused=error $(CHAPTERS_EN)
	touch $@

$(DESTDIR)/.check-lt-ru: $(CHECK_LANGUAGETOOL) $(LTEX_RU) $(CHAPTERS_RU)
	$(CHECK_LANGUAGETOOL) --lang ru-RU --unused=error $(CHAPTERS_RU)
	touch $@

$(DESTDIR)/.check-wc: $(CHECK_WC) $(CHAPTERS_EN) $(CHAPTERS_RU)
	$(CHECK_WC)
	touch $@
