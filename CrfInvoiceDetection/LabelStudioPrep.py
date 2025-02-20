def formatTokenForLabelStudio(tokens):
    dataText = "";
    result = [];
    for token in tokens:
        result.append({
            "type": "labels",
            "from_name": "label",
            "to_name": "text",
            "value": {
                "start": len(dataText) + 1,
                "end": len(dataText) + 1 + len(token),
                "text": token,
                "label": ["O"]
            }
        });
        dataText+= " " + token;
    labelStudioToken = [{
        "data": {"text": dataText},
        "annotations": [{"result": result}]
    }];
    return labelStudioToken;
