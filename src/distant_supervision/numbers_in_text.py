from stanford.corenlpy import SharedNERPipeline, Annotation, CoreAnnotations, NumberNormalizer, BigDecimal, Double


def numbers_in_text(text):
    doc = Annotation(text)
    SharedNERPipeline().getInstance().annotate(doc)
    numbers = []
    for sentence in doc.get(CoreAnnotations.SentencesAnnotation).toArray():
        NumberNormalizer.findNumbers(sentence)
        for corelabel in sentence.get(CoreAnnotations.TokensAnnotation).toArray():
            num = corelabel.get(CoreAnnotations.NumericCompositeValueAnnotation)
            if num is not None:
                numbers.append(num)
    return numbers


def sentences_with_numbers(text,target,thresh):
    doc = Annotation(text)
    SharedNERPipeline().getInstance().annotate(doc)

    sentences = []

    for sentence in doc.get(CoreAnnotations.SentencesAnnotation).toArray():
        NumberNormalizer.findNumbers(sentence)
        has_number = False
        tokens = []
        for corelabel in sentence.get(CoreAnnotations.TokensAnnotation).toArray():
            num = corelabel.get(CoreAnnotations.NumericCompositeValueAnnotation)
            if num is not None:
                has_number = True
                break
                if type(num) == BigDecimal:
                    num = Double.valueOf(num.toString())

                #if threshold_match(num,target,thresh):
                #    has_number = True


        if has_number:
            for corelabel in sentence.get(CoreAnnotations.TokensAnnotation).toArray():
                tok = corelabel.get(CoreAnnotations.TextAnnotation)
                tokens.append(tok)
            sentences.append(" ".join(tokens))

    return sentences

if __name__ == "__main__":
    numbers_in_text("In 1965, Jersey Standard started to acquire coal assets through its affiliate Carter Oil (later renamed: Exxon Coal, U.S.A.). For managing the Midwest and Eastern coal assets in the United States, the Monterey Coal Company was established in 1969. Carter Oil focused on the developing synthetic fuels from coal. In 1966, it started to developed the coal liquefaction process called the Exxon Donor Solvent Process. In April 1980, Exxon opened a 250-ton-per-day pilot plant in Baytown, Texas. The plant was closed and dismantled in 1982.")
    print(sentences_with_numbers(
        "This sentence has no numeric value. In 1965, Jersey Standard started to acquire coal assets through its affiliate Carter Oil (later renamed: Exxon Coal, U.S.A.). For managing the Midwest and Eastern coal assets in the United States, the Monterey Coal Company was established in 1969. Carter Oil focused on the developing synthetic fuels from coal. In 1966, it started to developed the coal liquefaction process called the Exxon Donor Solvent Process. In April 1980, Exxon opened a 250-ton-per-day pilot plant in Baytown, Texas. The plant was closed and dismantled in 1982."))

