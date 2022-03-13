import fitz
from pathlib import Path

doc_from= fitz.open("from.pdf")
doc_to= fitz.open("to.pdf")
output = Path("output2.pdf")


for i in range(doc_from.pageCount):

    page_from= doc_from[i]
    page_to= doc_to[i]

    for annot in page_from.annots():

        # cp Highlight annotations
        if (annot.type[1] == "Highlight"):

            # Highlight annots cannot have 4+ vertices
            # Divide the polygons containing the text to be highlighted into constituent rectangles
            # highlight each rectangle

            n = 0
            while n < len(annot.vertices) - 3:

                quad = fitz.Quad(
                fitz.Point(annot.vertices[n]),
                fitz.Point(annot.vertices[n+1]),
                fitz.Point(annot.vertices[n+2]),
                fitz.Point(annot.vertices[n+3]))

                highlight = page_to.add_highlight_annot(quad)

                #copy info from 'from' pdf to the annot class
                # also add content for popup
                highlight.set_info(
                title = annot.info["title"],
                subject = annot.info["subject"],
                creationDate = annot.info["creationDate"],
                modDate = annot.info["modDate"],
                content = annot.info["content"]
                )

                highlight.set_popup(annot.rect.quad)

                #save
                highlight.update()

                n += 4

        # cp Text (sticky note) annotations
        if (annot.type[1] == "Text"):

            #get point_like i.e the position of the sticky_note
            point_like = annot.rect.tl

            #create the text annot
            sticky_note = page_to.add_text_annot(point_like, annot.info["content"])

            #copy info from annot in page_from
            if (annot.info["content"] != ""):
                sticky_note.set_info(
                title = annot.info["title"],
                subject = annot.info["subject"],
                creationDate = annot.info["creationDate"],
                modDate = annot.info["modDate"],
                content = annot.info["content"]
                )

            #save
            sticky_note.update()

#save doc as output.pdf
doc_to.save(
    output,
    garbage=4,
    clean=True,
    deflate=True,
    deflate_images=True,
    deflate_fonts=True,
    )
