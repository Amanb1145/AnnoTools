import sys

sys.path.insert(0, '..')
from .helperfile import file_to_txt
import re
import os
import json
from django.http import JsonResponse


def return_annotated_file(path, ents):
    """ This function takes resume path and entities to be anotated in resume
        as input and returns the annotated JSON file.
        The entities should be passed as a list containing text and their 
        corresponding label like [(text1, label1), (text2, label2)].
    """
    resume_lines, _ = file_to_txt(path)
    full_text = " ".join(resume_lines)
    labels = []
    start_idx = []
    end_idx = {}
    texts = {}
    for text, label in ents:
        if text in texts.keys():
            texts[text] += 1
            try:
                find_text = re.search(text, full_text[end_idx[text]:])
                labels.append([find_text.span()[0], find_text.span()[1], label])
                start_idx.append(find_text.span()[0])
                end_idx[text] = find_text.span()[1]
            except:
                pass
        else:
            texts[text] = 1
            try:
                find_text = re.search(text, full_text)
                labels.append([find_text.span()[0], find_text.span()[1], label])
                start_idx.append(find_text.span()[0])
                end_idx[text] = find_text.span()[1]
            except:
                pass
    # print(start_idx, end_idx)
    print(texts, end_idx)
    return JsonResponse({"text": full_text, "labels": labels})
    # return json.dumps({
    #     "text": full_text,
    #     "labels": labels
    # })


#path = r'C:\Users\kramatur.r\Desktop\Kramatur_Resume.pdf'
#ents = [("kramatur Reza", "Name"),("Indus Business Academy","College"),("PGDM","Degree")]
#print(return_annotated_file(path, ents))
