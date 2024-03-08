import cv2 as cv
import datetime

target_format = 'avi'
target_fourcc = 'XVID'

video = cv.VideoCapture(0)
fps = video.get(cv.CAP_PROP_FPS)
wait_ms = int(1 / fps * 1000)
is_recording = False
flip_horizontal = False
flip_vertical = False

writer = cv.VideoWriter()

while True:
  valid, captured_image = video.read()
  if not valid:
    break

  final_image = captured_image.copy()

  if is_recording:
    if not writer.isOpened():
      target_file = f'{datetime.datetime.now()}.{target_format}'
      fps = video.get(cv.CAP_PROP_FPS)
      height, width, *_ = captured_image.shape
      is_color = (captured_image.ndim > 2) and (captured_image.shape[2]) > 1
      writer.open(target_file, cv.VideoWriter_fourcc(*target_fourcc), fps, (width, height), is_color)
      assert writer.isOpened(), f'Cannot open the video file: {target_file}'
    writer.write(captured_image)
    cv.circle(final_image, (50, 50), 20, (0, 0, 255), thickness=-1)

  if flip_vertical and flip_horizontal:
    final_image = cv.flip(final_image, -1)
  elif flip_vertical:
    final_image = cv.flip(final_image, 0)
  elif flip_horizontal:
    final_image = cv.flip(final_image, 1)
  cv.imshow('OpenCV Video Recorder', final_image)

  key = cv.waitKey(max(wait_ms, 1))
  if key == 27:
    break
  elif key == ord(' '):
    if is_recording is True:
      writer.release()
    is_recording = not is_recording
  elif key == ord('h'):
    flip_horizontal = not flip_horizontal
    print(flip_horizontal)
  elif key == ord('v'):
    flip_vertical = not flip_vertical

writer.release()