from ultralytics import YOLO
import cv2
import streamlit as st
import yt_dlp
import settings


# ---------------- Load Model ----------------
def load_model(model_path):
    """Load YOLO model from given path."""
    return YOLO(str(model_path))


# ---------------- Tracker Options ----------------
def display_tracker_options():
    display_tracker = 'No'  # st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None


# ---------------- Frame Display ----------------
def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Run YOLO detection/tracking on a frame and display via Streamlit.
    """
    # Resize for display
    h, w = image.shape[:2]
    target_w = 720
    scale = target_w / max(1, w)
    target_h = int(h * scale)
    image_resized = cv2.resize(image, (target_w, target_h))

    # Detection / Tracking
    if is_display_tracking:
        res = model.track(image_resized, conf=conf, persist=True, tracker=tracker)
    else:
        res = model.predict(image_resized, conf=conf)

    # Plot & Display
    res_plotted = res[0].plot()
    st_frame.image(
        res_plotted,
        caption="Detected Video",
        channels="BGR",
        use_column_width=True
    )


# ---------------- YouTube Stream ----------------
def _get_youtube_stream_url(url: str) -> str:
    """
    Extract direct stream URL from YouTube (without full download).
    """
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "nocheckcertificate": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


def play_youtube_video(conf, model):
    source_youtube = st.sidebar.text_input("YouTube Video URL")
    is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button("Detect Objects", key="yt"):
        if not source_youtube:
            st.sidebar.error("Please paste a YouTube URL")
            return
        try:
            stream_url = _get_youtube_stream_url(source_youtube)
            vid_cap = cv2.VideoCapture(stream_url)

            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, is_display_tracker, tracker)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading YouTube stream: " + str(e))


# ---------------- RTSP Stream ----------------
def play_rtsp_stream(conf, model):
    """
    Plays an RTSP stream and detects objects using YOLOv8.
    """
    source_rtsp = st.sidebar.text_input("RTSP stream URL:")
    st.sidebar.caption("Example: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101")
    is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button("Detect Objects", key="rtsp"):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()

            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, is_display_tracker, tracker)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))


# ---------------- Webcam ----------------
def play_webcam(conf, model):
    """
    Plays webcam stream and detects objects using YOLOv8.
    """
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button("Detect Objects", key="webcam"):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()

            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf, model, st_frame, image, is_display_tracker, tracker)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading webcam: " + str(e))
