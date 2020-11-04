import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os, urllib, cv2

from pram.data   import GroupSizeProbe, ProbeMsgMode
from pram.entity import Group, GroupQry, GroupSplitSpec, Site
from pram.rule   import GoToRule, DiscreteInvMarkovChain, TimeInt
from pram.sim    import Simulation

# Streamlit encourages well-structured code, like starting execution in a main() function.
def main():
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown("#PRAM WEBSERVER v2")

    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    st.sidebar.title("PRAM WEB v2")
    app_mode = st.sidebar.selectbox("Choose simulation",
        ["Show instructions", "01-simple", "Show the source code"])
    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "Show the source code":
        readme_text.empty()
        st.code("# EMPTY")
    elif app_mode == "01-simple":
        readme_text.empty()
        run_the_app()

# This is the main app app itself, which appears when the user selects "Run the app".
def run_the_app():

    # Draw the UI elements to search for objects (pedestrians, cars, etc.)
    gsize, s1, s2, s3, i1, i2, i3, r1, r2, r3 = frame_selector_ui()

    progress_flu_rule = DiscreteInvMarkovChain('flu-status',
    { 's': [s1, s2, s3], 'i': [i1, i2, i3], 'r': [r1, r2, r3] })
    # s - susceptible
    # i - infectious
    # r - recovered

    sites = { 'home': Site('h'), 'work': Site('w') }

    probe_grp_size_flu = GroupSizeProbe.by_attr('flu', 'flu-status', progress_flu_rule.get_states(), msg_mode=ProbeMsgMode.DISP, memo='Mass distribution across flu status')
    probe_grp_size_site = GroupSizeProbe.by_rel('site', Site.AT, sites.values(), msg_mode=ProbeMsgMode.DISP, memo='Mass distribution across sites')

    data = ""
    s = Simulation()
    s.add_rule(progress_flu_rule)
    s.add_probe(probe_grp_size_flu)
    s.add_group(Group('g0', gsize, { 'flu-status': 's' }))
    sys.stdout = open('out.dat', 'w')
    s.run(24)
    sys.stdout.close()

    with open('out.dat') as file:
        data = file.readlines()
        data = str(self.data)
    st.write(data)

# This sidebar UI is a little search engine to find certain object types.
def frame_selector_ui():
    st.sidebar.markdown("# Paramaters")

    # Choose a frame out of the selected frames.
    gsize = st.sidebar.slider("Choose group size ", 1, 10000, 0)

    st.sidebar.markdown("### Susceptible")
    s1 = st.sidebar.number_input("[x,_, _]", key="s1")
    s2 = st.sidebar.number_input("[_,x,_]", key="s2")
    s3 = st.sidebar.number_input("[_,_,x]", key="s3")


    st.sidebar.markdown("### Infectious")
    i1 = st.sidebar.number_input("[x,_, _]", key="i1")
    i2 = st.sidebar.number_input("[_,x,_]", key="i2")
    i3 = st.sidebar.number_input("[_,_,x]", key="i3")


    st.sidebar.markdown("### Recovered")
    r1 = st.sidebar.number_input("[x,_, _]", key="r1")
    r2 = st.sidebar.number_input("[_,x,_]", key="r2")
    r3 = st.sidebar.number_input("[_,_,x]", key="r3")
    return gsize, s1, s2, s3, i1, i2, i3, r1, r2, r3

# Select frames based on the selection in the sidebar
@st.cache(hash_funcs={np.ufunc: str})
def get_selected_frames(summary, label, min_elts, max_elts):
    return summary[np.logical_and(summary[label] >= min_elts, summary[label] <= max_elts)].index

# This sidebar UI lets the user select parameters for the YOLO object detector.
def object_detector_ui():
    st.sidebar.markdown("# Model")
    confidence_threshold = st.sidebar.slider("Confidence threshold", 0.0, 1.0, 0.5, 0.01)
    overlap_threshold = st.sidebar.slider("Overlap threshold", 0.0, 1.0, 0.3, 0.01)
    return confidence_threshold, overlap_threshold

# Draws an image with boxes overlayed to indicate the presence of cars, pedestrians etc.
def draw_image_with_boxes(image, boxes, header, description):
    # Superpose the semi-transparent object detection boxes.    # Colors for the boxes
    LABEL_COLORS = {
        "car": [255, 0, 0],
        "pedestrian": [0, 255, 0],
        "truck": [0, 0, 255],
        "trafficLight": [255, 255, 0],
        "biker": [255, 0, 255],
    }
    image_with_boxes = image.astype(np.float64)
    for _, (xmin, ymin, xmax, ymax, label) in boxes.iterrows():
        image_with_boxes[int(ymin):int(ymax),int(xmin):int(xmax),:] += LABEL_COLORS[label]
        image_with_boxes[int(ymin):int(ymax),int(xmin):int(xmax),:] /= 2

    # Draw the header and image.
    st.subheader(header)
    st.markdown(description)
    st.image(image_with_boxes.astype(np.uint8), use_column_width=True)

# Download a single file and make its content available as a string.
@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/streamlit/demo-self-driving/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

# This function loads an image from Streamlit public repo on S3. We use st.cache on this
# function as well, so we can reuse the images across runs.
@st.cache(show_spinner=False)
def load_image(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[:, :, [2, 1, 0]] # BGR -> RGB
    return image

# Run the YOLO model to detect objects.
def yolo_v3(image, confidence_threshold, overlap_threshold):
    # Load the network. Because this is cached it will only happen once.
    @st.cache(allow_output_mutation=True)
    def load_network(config_path, weights_path):
        net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        output_layer_names = net.getLayerNames()
        output_layer_names = [output_layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return net, output_layer_names
    net, output_layer_names = load_network("yolov3.cfg", "yolov3.weights")

    # Run the YOLO neural net.
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layer_names)

    # Supress detections in case of too low confidence or too much overlap.
    boxes, confidences, class_IDs = [], [], []
    H, W = image.shape[:2]
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidence_threshold:
                box = detection[0:4] * np.array([W, H, W, H])
                centerX, centerY, width, height = box.astype("int")
                x, y = int(centerX - (width / 2)), int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_IDs.append(classID)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, overlap_threshold)

    # Map from YOLO labels to Udacity labels.
    UDACITY_LABELS = {
        0: 'pedestrian',
        1: 'biker',
        2: 'car',
        3: 'biker',
        5: 'truck',
        7: 'truck',
        9: 'trafficLight'
    }
    xmin, xmax, ymin, ymax, labels = [], [], [], [], []
    if len(indices) > 0:
        # loop over the indexes we are keeping
        for i in indices.flatten():
            label = UDACITY_LABELS.get(class_IDs[i], None)
            if label is None:
                continue

            # extract the bounding box coordinates
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]

            xmin.append(x)
            ymin.append(y)
            xmax.append(x+w)
            ymax.append(y+h)
            labels.append(label)

    boxes = pd.DataFrame({"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax, "labels": labels})
    return boxes[["xmin", "ymin", "xmax", "ymax", "labels"]]

# Path to the Streamlit public S3 bucket
DATA_URL_ROOT = "https://streamlit-self-driving.s3-us-west-2.amazonaws.com/"

# External files to download.
EXTERNAL_DEPENDENCIES = {
    "yolov3.weights": {
        "url": "https://pjreddie.com/media/files/yolov3.weights",
        "size": 248007048
    },
    "yolov3.cfg": {
        "url": "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg",
        "size": 8342
    }
}

if __name__ == "__main__":
    main()
