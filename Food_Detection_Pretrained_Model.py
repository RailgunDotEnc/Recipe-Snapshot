import requests
from PIL import Image
import torch

from transformers import OwlViTProcessor, OwlViTForObjectDetection

"These are the food ideas of what we will train Bread, Milk, Eggs, rice, tortillas, frijoles"

def scanimage(self,img=r"C:\Users\danie\Downloads\OIP.jpg"):
    mylist=[]
    dic_results={0:"bread",1:"milk",2:"egg", 3:"rice", 4: "tortilla", 5: "bean"}
    return_list=[]
    
    processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
    model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")
    pretext="a picture of a "
    image = Image.open(img)
    texts=[[]]
    for i in range(len(dic_results)):
        texts[0].append(f"{pretext}{dic_results[i]}")
    inputs = processor(text=texts, images=image, return_tensors="pt")
    outputs = model(**inputs)
    
    # Target image sizes (height, width) to rescale box predictions [batch_size, 2]
    target_sizes = torch.Tensor([image.size[::-1]])
    # Convert outputs (bounding boxes and class logits) to COCO API
    results = processor.post_process(outputs=outputs, target_sizes=target_sizes)
    
    i = 0  # Retrieve predictions for the first image for the corresponding text queries
    text = texts[i]
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]
    
    score_threshold = 0.1
    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        if score >= score_threshold:
            for i in range (len(texts[0])):
                if texts[0][i] in text[label] and i not in mylist:
                    mylist.append(i)
                    self.text_event(f"Detected {text[label]} with confidence {round(score.item(), 3)} at location {box}")
    self.text_event("Found")
    for i in range(len(mylist)):
        self.text_event(dic_results[mylist[i]])
        return_list.append(dic_results[mylist[i]])
    self.set_ingredients(return_list)
