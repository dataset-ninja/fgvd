The authors introduce the **FGVD: Fine-Grained Vehicle Detection Dataset**, captured from a moving camera mounted on a car. It contains 5502 scene images with 210 unique fine-grained labels of multiple vehicle types organized in a three-level hierarchy. While previous classification datasets also include makes for different kinds of cars, the FGVD dataset introduces new class labels for categorizing two-wheelers, autorickshaws, and trucks. The FGVD dataset is challenging as it has vehicles in complex traffic scenarios with intra-class and inter-class variations.

Note, similar **FGVD: Fine-Grained Vehicle Detection Dataset** datasets are also available on the [DatasetNinja.com](https://datasetninja.com/):

- [IDD: Object Detection Dataset](https://datasetninja.com/idd-detection)

## Motivation

Intelligent traffic monitoring systems are of utmost need in big cities for public security, planning, and surveillance. For the tasks like vehicle re-identification and robust detection (e.g., when a vehicle occludes another vehicle that is similar in appearance), the detectors used in the surveillance systems should finely classify the vehicle type, ***manufacturer***, and ***model*** of the on-road vehicles. Conventionally, detection models are trained to classify vehicles based on coarse categories of on-road datasets. A coarse class can contain multiple sub-classes with minute variations, referred to as the fine-grained classes. The localization of such sub-class vehicles based on their granularity in the design is known as Fine-Grained Vehicle Detection. The FGVD models and datasets can enable robust vehicle re-identification and detection in highly dense and occluded traffic scenarios. 

## Dataset description

The authors propose a novel FGVD dataset with multiple hierarchy levels for the fine-grained labels. In addition to enabling the detection task, the FGVD dataset includes complex intra-class and inter-class variations in types, scales, and orientations compared to the previous fine-grained classification datasets.

<img src="https://github.com/dataset-ninja/fgvd/assets/120389559/1506be28-780f-47d9-a5e2-3638f04cb69e" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Fine-grained datasets samples. Top: Previous datasets focus only on the classification of cars on vehicle centric images. Middle: The proposed FGVD dataset enables fine-grained (multi) vehicle detection on unconstrained road scenes captured from vehicle-mounted cameras. Bottom left GradCAM++ visualizations on predicted crops show that the model focuses on the backlight and blinker at the motorcycle’s top and scooter’s bottom. For Tavera, the design on the left and right of license plates, and for Ciaz, the radiator and headlight regions are highlighted classification features.</span>

The dataset also contains challenging occlusion scenarios and lighting conditions. FGVD comprises three levels of hierarchy, i.e., vehicle type, ***manufacturer***, and ***model***.

<img src="https://github.com/dataset-ninja/fgvd/assets/120389559/0f74df29-0c8d-46a0-bf6f-24b512f45348" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Sample images of different categories in FGVD exhibiting inter-class similarities (bottom two rows), multiple vehicle orientations (all rows), and frequent occlusions.</span>

The authors introduce the complementary hierarchical labels for two-wheelers, *autorickshaws*, *trucks*, and *buses*. The granularity of the FGVD dataset increases as they move from parent to child level. For the hierarchical FGVD dataset, every level has its uniqueness. Firstly, different vehicles may look similar at the first level of granularity, e.g., *motorcycles* and *scooters*, both being the two-wheelers. However, the overall design of the scooter is different from the *motorcycle*, e.g., *scooters* have a backlight at the bottom as compared to the top backlight of the *motorcycle*. The overall appearance of the two vehicles with the same parent may look even more similar. However, the minute subtle and local differences are present in the same subcategory. Also,  some categories are not present in the earlier vehicle datasets, for example, *scooter*, *autorickshaw*, *truck*, and *bus*; hence, they must be added to a fine-grained dataset. Therefore, the authors introduce classes unique to the FGVD dataset to facilitate detailed research in fine-grained on-road scenarios. 

## Dataset acquisition

The authors utilize images paired with coarse labels and bounding boxes sourced from the [IDD detection](http://idd.insaan.iiit.ac.in/) dataset. However, annotating vehicles situated far from the camera proves impractical. Consequently, they filter out bounding boxes with height-to-width ratios below specified thresholds, adjusted to accommodate the varying dimensions of vehicle types. To streamline annotation efforts, they set higher threshold values for *trucks*, followed by *cars* and *bikes*. This thresholding approach simplifies the annotators' task, rendering it more manageable and efficient. The FGVD dataset comprises 5,502 scene images encompassing approximately 24,450 bounding boxes, annotated with 217 fine-grained labels at the third level, including 210 unique labels and 7 repetitions from higher levels.

From the IDD Detection dataset, the authors curate 5,502 high-quality images out of 16,311 based on factors like occlusion, vehicle box size, and traffic density. An annotation team comprising four skilled annotators and two expert reviewers oversees the process, ensuring quality control. Initially, annotators receive training on fine-grained labeling using select FGVD samples. They are then provided with guidelines, templates, and a list of objects for annotation. Following comprehensive training, annotators can identify popular vehicles within scenes. In cases where recognition proves challenging, annotators resort to tools like [Google Lens](https://lens.google/) or online image searches. For instance, if a vehicle's ***model*** name is obscured but the brand logo is visible, annotators may search for similar vehicles on the ***manufacturer***'s website to aid identification. Notably, the IDD-Detection dataset incorporates images captured from continuous video frames, establishing a temporal connection. This temporal context aids in labeling vehicles, even when their design is not fully discernible in isolated frames. Annotators leverage information from different frames to propagate labels, enhancing accuracy, particularly in instances of occlusion or truncation.

<img src="https://github.com/dataset-ninja/fgvd/assets/120389559/683d24d1-1ede-4cf3-8832-6b21968feccf" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Annotation Strategy: (b) is the only confidently identifiable image frame where the label cue (logo at bottom-left of the car) is visible. As the frames are from common video sequence, the label is propagated to the vehicle instances in (a), \(c\) & (d).</span>

The authors implement a two-step approach in the data creation process, consisting of the pilot phase and the takeoff phase. During the pilot phase, each annotator works on a small subset of images characterized by lower traffic density. Additionally, they provide training to annotators on labeling vehicles that are confidently identifiable but lack bounding boxes. For *cars*, *motorcycles*, and *scooters*, a special attribute labeled "new" is introduced to identify new variants encountered in the dataset. Annotators mark this attribute whenever they encounter such variants.

Subsequently, all labels generated during the takeoff stage undergo review. Images with labels marked with high confidence by reviewers are retained for inclusion in the dataset. Any vehicle bounding boxes remaining ambiguous at fine-grained levels are categorized as "others." Instances where vehicles are partially obscured by materials like covers or cloth are labeled as "covered."

## Classes hierarchy

Each vehicle type in the proposed Fine-Grained Vehicle Detection (FGVD) dataset has different hierarchical levels. The FGVD contains three different levels of hierarchy: 

* **Vehicle-type:** The highest coarse level labels of the vehicle come under the vehicle-type category. The authors consider it as level 1 of the hierarchy. *car*, *motorcycle*, *scooter*, *truck*, *autorickshaw*, *bus* and *mini-bus* are the six categories present in vehicle type.
* **Manufacturer:** The ***manufacturer*** level contains the primary producer of the vehicles. The ***manufacturer*** category has finer details than the vehicle type level. A producer may manufacture multiple kinds of vehicles. For example, Bajaj manufactures *motorcycles* as well as *autorickshaw*.
* **Model:** The ***model*** level is at the last group of the hierarchy. This level comprises highly fine-grained features that are unique for the variant. For example, a car’s design must be unique for each ***manufacturer***.

<img src="https://github.com/dataset-ninja/fgvd/assets/120389559/132276fc-3ce2-42f1-b404-0544c588e897" alt="image" width="600">

<span style="font-size: smaller; font-style: italic;">Sample Hierarchy Tree of the FGVD dataset.</span>

| Vehicle Type  | Levels of Hierarchy | L-2 labels | L-3 labels |
|---------------|----------------------|------------|------------|
| Car           | 3                    | 22         | 112        |
| Motorcycle    | 3                    | 11         | 67         |
| Scooter       | 3                    | 9          | 23         |
| Truck         | 2                    | 7          | 7          |
| Autorickshaw  | 2                    | 6          | 6          |
| Bus           | 2                    | 2          | 2          |
| Total         | 3                    | 57         | 217        |

<span style="font-size: smaller; font-style: italic;">Levels of Hierarchy for different Vehicles in FGVD.</span>

