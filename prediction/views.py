from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from django.shortcuts import render

def home(request):
    return render(request, "prediction/test2.html")

# Load the model once when Django starts
MODEL_FILE = os.path.join(os.path.dirname(__file__), "../efficientnet_skin_model_final.keras")

if os.path.exists(MODEL_FILE):
    model = load_model(MODEL_FILE)
else:
    model = None  # Handle missing model gracefully

# Define class labels and descriptions
disease_descriptions = {
    "akiec": "Actinic keratoses (AK) and intraepithelial carcinoma are precancerous skin conditions caused by prolonged sun exposure. They typically appear as rough, scaly, red or brown patches on sun-exposed areas like the face, scalp, and hands. AK is considered an early warning sign of potential skin cancer, particularly squamous cell carcinoma. These lesions can sometimes be itchy, tender, or inflamed, making early diagnosis crucial. Discovered in the early 20th century, AK is one of the most common precancerous conditions affecting millions worldwide, particularly older individuals with fair skin.\n\nAlthough actinic keratosis itself is not life-threatening, if left untreated, it can progress into invasive squamous cell carcinoma, which can be dangerous. The risk increases with cumulative sun exposure, genetic predisposition, and weakened immune systems. Diagnosis is typically made through clinical examination, and in uncertain cases, a biopsy may be performed. Patients are advised to wear sunscreen and protective clothing to reduce further sun damage and slow the progression of existing lesions.\n\nTreatment options for AK include cryotherapy (freezing the lesion with liquid nitrogen), laser therapy, and topical medications such as 5-fluorouracil (5-FU), imiquimod, or diclofenac. Intraepithelial carcinoma, also known as Bowen’s disease, may require surgical excision or photodynamic therapy in more advanced cases. Regular follow-ups with a dermatologist are essential to monitor and manage new or changing lesions. Prevention strategies include using broad-spectrum sunscreen and avoiding peak sun hours to reduce UV exposure.\n",

    "bcc": "Basal cell carcinoma (BCC) is the most common type of skin cancer, primarily caused by long-term exposure to ultraviolet (UV) radiation. It typically appears as a pearly or waxy bump, an open sore, or a reddish patch that does not heal. Unlike other skin cancers, BCC grows slowly and rarely spreads to other parts of the body, but if left untreated, it can invade deeper tissues, leading to significant damage. First identified in the 19th century, BCC is more common in fair-skinned individuals and those with excessive sun exposure.\n\nThough not life-threatening in most cases, BCC can be locally aggressive and cause tissue destruction if neglected. Risk factors include excessive sun exposure, fair skin, previous radiation therapy, and a family history of skin cancer. Dermatologists usually diagnose BCC through visual examination and biopsy, and early detection ensures better treatment outcomes. Patients with a history of BCC should schedule regular skin checks to detect recurrence or new lesions.\n\nTreatment options for BCC depend on its size, location, and depth. The most effective method is Mohs micrographic surgery, which ensures complete removal while preserving healthy skin. Other treatments include excisional surgery, cryotherapy, radiation therapy, and topical medications like imiquimod or 5-fluorouracil. In advanced or recurrent cases, targeted drugs such as vismodegib and sonidegib may be prescribed. Preventative measures include avoiding prolonged sun exposure, wearing sunscreen, and using protective clothing.\n",

    "bkl": "Benign keratosis-like lesions (BKL) refer to non-cancerous skin growths, including seborrheic keratoses, solar lentigines, and lichen planus-like keratoses. These lesions appear as brown, black, or tan waxy patches that may resemble warts. They are primarily associated with aging and long-term sun exposure. Although they might look concerning, they are harmless and do not develop into cancer. First studied in the late 19th century, these lesions are extremely common in individuals over 50, especially in fair-skinned people.\n\nDespite their harmless nature, some benign keratoses may resemble melanoma or other malignant skin conditions, necessitating a dermatological evaluation. The primary risk factors include genetics, UV exposure, and age-related skin changes. While BKL does not require treatment, people may seek removal for cosmetic reasons or if the lesion becomes irritated or itchy. A doctor may recommend a biopsy if the lesion changes rapidly or has an unusual appearance.\n\nTreatment options include cryotherapy (freezing), laser therapy, electrosurgery, or curettage. Topical retinoids may sometimes help reduce pigmentation in solar lentigines. While no medication is necessary for most cases, maintaining proper sun protection and skin hydration can help prevent new lesions. People with multiple seborrheic keratoses should undergo periodic skin evaluations to rule out potential malignancies.\n",

    "df": "Dermatofibroma is a common benign skin tumor that presents as a small, firm, reddish-brown or dark bump on the skin. It is composed of fibrous tissue and usually forms on the legs. Dermatofibromas are more frequently seen in women and often develop after minor trauma, such as insect bites or ingrown hairs. First documented in the early 20th century, dermatofibromas are harmless and do not require treatment unless they become bothersome or painful.\n\nAlthough dermatofibromas are benign, their firm attachment to deeper layers of skin can cause a dimpling effect when pinched. They are not contagious and do not spread to other areas. The cause of these growths is not fully understood, but they are believed to result from an overgrowth of fibroblasts, the cells responsible for skin repair. Diagnosis is typically clinical, and a biopsy may be performed if the lesion appears atypical.\n\nMost dermatofibromas do not require treatment, but if they become painful or cosmetically undesirable, they can be removed via surgical excision, cryotherapy, or laser therapy. No medications are typically required for treatment, but some individuals may use topical corticosteroids if inflammation occurs. Regular skin checks are advised, especially if new lesions develop or if an existing lesion changes in appearance.\n",

    "mel": "Melanoma is an aggressive and potentially deadly form of skin cancer that originates from melanocytes, the cells responsible for skin pigmentation. It typically appears as an irregular, dark, and rapidly growing mole with asymmetrical borders. Melanoma is highly invasive and can spread to lymph nodes and other organs if not detected early. First identified in the early 19th century, melanoma accounts for a small percentage of skin cancers but causes the majority of skin cancer-related deaths worldwide.\n\nThe primary risk factors for melanoma include excessive sun exposure, genetic predisposition, fair skin, and a history of sunburns. Dermatologists use the ABCDE rule (Asymmetry, Border irregularity, Color variation, Diameter over 6mm, and Evolving changes) to identify suspicious moles. A skin biopsy is the definitive method for diagnosis, and early detection significantly improves survival rates. Regular skin screenings and self-examinations are crucial for high-risk individuals.\n\nTreatment for melanoma varies based on its stage. Early-stage melanomas are treated with surgical excision, while advanced cases may require immunotherapy (nivolumab, pembrolizumab), targeted therapy (BRAF/MEK inhibitors), or chemotherapy. Radiation therapy may be used in some cases. Preventative measures include avoiding UV exposure, using broad-spectrum sunscreen, and wearing protective clothing. Early detection remains the key to successful treatment and long-term survival.\n",

    "vasc": "Vascular lesions refer to a group of abnormalities affecting the blood vessels in the skin, including hemangiomas, angiomas, and telangiectasias. These lesions appear as red, purple, or blue marks on the skin due to abnormal blood vessel growth or dilation. They can be congenital (present from birth) or develop over time due to aging, sun exposure, or hormonal changes. First documented in the early 20th century, vascular lesions are generally benign but may sometimes indicate underlying vascular disorders.\n\nMost vascular lesions are harmless and do not require treatment, but in some cases, they can bleed, cause discomfort, or affect appearance. The primary risk factors include genetics, prolonged sun exposure, hormonal changes (such as pregnancy), and certain medical conditions. Diagnosis is typically made through dermatological examination and dermoscopy, with imaging tests like Doppler ultrasound used for deeper or complex lesions. Some vascular lesions, such as spider angiomas, are linked to liver disease and may warrant further investigation.\n\nTreatment options depend on the type and severity of the lesion. Small, harmless lesions may be left untreated, while bothersome or cosmetically concerning ones can be removed using laser therapy, sclerotherapy, or electrosurgery. Topical treatments like beta-blockers (propranolol) or corticosteroids may be used in some cases, especially for infantile hemangiomas. Preventative measures include protecting the skin from excessive sun exposure and monitoring new or changing vascular spots. While most vascular lesions remain stable, any sudden changes should be evaluated by a dermatologist.\n",

    "nv": "Melanocytic nevus (NV), commonly referred to as a mole, is a benign growth of melanocytes, the pigment-producing cells in the skin. Moles can be present at birth (congenital) or develop over time (acquired) due to genetic factors and sun exposure. They usually appear as small, round, or oval-shaped brown, black, or flesh-colored spots with well-defined borders. Although most moles are harmless, some may evolve into atypical nevi, which have irregular shapes and color variations, raising concerns for potential melanoma. The first medical documentation of melanocytic nevi dates back centuries, with their study advancing significantly in the 19th and 20th centuries.\n\nMoles can vary in size and may darken with sun exposure, hormonal changes (such as pregnancy), or age. While most remain stable, some may grow, become itchy, or change in appearance, necessitating medical evaluation. Dermatologists use dermoscopy to analyze mole structures and determine whether a biopsy is necessary. Individuals with many moles, a family history of melanoma, or fair skin are at a higher risk of developing skin cancer. Regular skin self-examinations and professional check-ups are recommended for early detection of abnormal changes.\n\nTreatment for benign moles is typically unnecessary unless they cause irritation or are cosmetically undesirable. If a mole is suspected to be precancerous or malignant, it can be removed via surgical excision or shave biopsy. In cases where melanoma is a concern, further analysis and potential additional treatments may be required. Preventative measures include wearing sunscreen, avoiding excessive UV exposure, and monitoring moles for any suspicious changes using the ABCDE rule (Asymmetry, Border irregularity, Color variation, Diameter over 6mm, and Evolving nature). Early intervention can help prevent potential complications related to melanoma.\n"
}



CLASS_LABELS = list(disease_descriptions.keys())  # Use the keys from the dictionary

def predict(request):
    """ Handles image upload and prediction """
    if request.method == 'POST' and request.FILES.get('image'):
        img_file = request.FILES['image']
        
        # Save the uploaded image properly
        temp_path = default_storage.save("uploads/" + img_file.name, ContentFile(img_file.read()))
        file_path = default_storage.path(temp_path)

        # Ensure the file exists
        if not os.path.exists(file_path):
            return JsonResponse({"error": "Failed to save image file"}, status=500)

        # Load and preprocess the image
        img = image.load_img(file_path, target_size=(224, 224))  # Adjust size if needed
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

        # Check if model is loaded
        if model is None:
            return JsonResponse({"error": "Model file not found!"}, status=500)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]  # Get class index
        disease_name = CLASS_LABELS[predicted_class] if predicted_class < len(CLASS_LABELS) else "Unknown"
        disease_description = disease_descriptions.get(disease_name, "No description available.")

        return JsonResponse({"disease": disease_name, "description": disease_description})

    return JsonResponse({"error": "Invalid request"}, status=400)




