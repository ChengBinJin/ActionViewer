import numpy as np
import cv2
import re
import sys

from ICVL_action_structure import int2stringLabel, readIcon


class ICVL:
    def __init__(self, video_id, path, resize_ratio=1.0, interval_time=1):
        self.resizeRatio = resize_ratio
        self.intervalTime = interval_time
        self.total_frames = 0
        
        self.videoID = video_id
        self.path = path
        self.GTPath = self.path[:-3] + 'txt'
        
        self.GT = []  # frame number, head_x, head_y, feet_x, feet_y, objc, objId, 1st_stage, 2nd_stage,
        # 3rd_stage, 4th_stage
        self.color = (0, 51, 255)
        self.thickness = 3
        
        self.fontFace = cv2.FONT_HERSHEY_TRIPLEX
        self.fontColor = (255, 255, 255)
        self.fontScale = 1.0 * self.resizeRatio
        self.fontThickness = 1
        
        self.icons = readIcon()    
        self.videoTime = self.get_video_time()
        
        self.stop_flag = False
        self.view_flag = True
        self.control = False

        self.video_cap = []
        self.read_frames()  # read all of the frames first

    def read_frames(self):
        video_cap = cv2.VideoCapture(self.path)
        if video_cap.isOpened() is False:
            print("Can not open video!")
            return 0

        while True:
            ret, raw_frame = video_cap.read()
            if ret is False:
                print("Can't read the frame")
                break

            self.video_cap.append(raw_frame)

        fps = int(video_cap.get(cv2.CAP_PROP_FPS))
        self.total_frames = len(self.video_cap)
        self.videoTime = self.total_frames // fps

        print("\nFinish to read Video ", self.videoID)
        print("Total frames: ", self.total_frames)

        # When everything done, release the capture
        video_cap.release()

    def get_video_time(self):
        video_cap = cv2.VideoCapture(self.path)
        if video_cap.isOpened() is False:
            print("Can not open video!")
            return 0
        
        total_frame = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video_cap.get(cv2.CAP_PROP_FPS))

        # When everything done, release the capture
        video_cap.release()

        return total_frame // fps

    def read_gt(self):
        with open(self.GTPath) as f:
            f.readline()  # throw away the first line that is information
            for line in f:
                data_list = [int(data) for data in re.split(r'\t+', line.rstrip('\t'))]
                self.GT.append(data_list)

        # print("Length:", len(self.GT))
        f.close()  # close file
        
    def show(self):
        cv2.namedWindow(self.path[-25:], cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(self.path[-25:], 300, 50)

        frame_id = 0
        while True:
            if frame_id < self.total_frames:
                raw_frame = self.video_cap[frame_id]
            else:
                break

            print("Frame: ", frame_id)

            raw_frame = cv2.resize(raw_frame, (int(self.resizeRatio * raw_frame.shape[1]),
                                               int(self.resizeRatio * raw_frame.shape[0])))
            show_frame = raw_frame.copy()
            show_frame = self.draw(show_frame, frame_id)

            if self.view_flag:
                cv2.imshow(self.path[-25:], show_frame)  # Display the resulting frame
            else:
                cv2.imshow(self.path[-25:], raw_frame)
            
            if self.stop_flag is False:
                asc_code = cv2.waitKey(self.intervalTime) & 0xFF
                if asc_code == ord('z'):
                    break
                elif asc_code == 27:  # Esc button
                    sys.exit("Esc clicked!")
                elif asc_code == ord(' '):
                    self.stop_flag = True
                elif asc_code == ord('v'):
                    self.view_flag = not self.view_flag
                else:
                    frame_id = frame_id + 1
            else:
                asc_code = cv2.waitKey(0) & 0xFF
                if asc_code == ord(' '):
                    self.stop_flag = False
                elif asc_code == ord('z'):
                    break
                elif asc_code == ord('e'):
                    frame_id = self.check_frame_id(frame_id, 30, self.total_frames)
                elif asc_code == ord('q'):
                    frame_id = self.check_frame_id(frame_id, -30, self.total_frames)
                elif asc_code == ord('d'):
                    frame_id = self.check_frame_id(frame_id, 1, self.total_frames)
                elif asc_code == ord('a'):
                    frame_id = self.check_frame_id(frame_id, -1, self.total_frames)
                elif asc_code == ord('v'):
                    self.view_flag = not self.view_flag
                elif asc_code == 27:  # Esc button
                    sys.exit("Esc clicked")

        cv2.destroyAllWindows()
        print("Finish to process!")
    
    @staticmethod
    def check_frame_id(frame_id, base, total_frame):
        temp = frame_id + base
        if 0 <= temp < total_frame:
            return temp
        else:
            return frame_id
        
    def draw(self, frame, number):
        show_frame = frame.copy()
        for index in range(len(self.GT)):
            if number == self.GT[index][0]:
                gt = self.GT[index].copy()

                # according to resize ratio
                gt[1] = int(self.resizeRatio * gt[1])
                gt[2] = int(self.resizeRatio * gt[2])
                gt[3] = int(self.resizeRatio * gt[3])
                gt[4] = int(self.resizeRatio * gt[4])
                
                show_frame = cv2.rectangle(show_frame, (gt[1], gt[2]), (gt[3], gt[4]),
                                           self.color, self.thickness)
                
                show_frame = self.fancy_show(show_frame, gt)  # show labels
                
        return show_frame
   
    @staticmethod
    def fancy_show_grid(frame, gt):
        grid = 0
        height, width, _ = frame.shape
        
        center_x = int((gt[1] + gt[3]) / 2.0)
        center_y = int((gt[2] + gt[4]) / 2.0)
        
        if (center_x <= width / 2.0) and (center_y <= height / 2.0):
            grid = 2
        elif (center_x <= width / 2.0) and (center_y > height / 2.0):
            grid = 3
        elif (center_x > width / 2.0) and (center_y <= height / 2.0):
            grid = 1
        elif (center_x > width / 2.0) and (center_y > height / 2.0):
            grid = 4
        
        return grid
        
    def fancy_show(self, show_frame, gt):
        # showFrame = frame.copy()
        
        obj_id = gt[6]
        # print("Object ID: ", obj_id)

        first, second, third, fourth = int2stringLabel(gt)  # int label to string label
                
        first_size = cv2.getTextSize(first, self.fontFace, self.fontScale,
                                     self.fontThickness)
        second_size = cv2.getTextSize(second, self.fontFace, self.fontScale,
                                      self.fontThickness)
        third_size = cv2.getTextSize(third, self.fontFace, self.fontScale,
                                     self.fontThickness)
        fourth_size = cv2.getTextSize(fourth, self.fontFace, self.fontScale,
                                      self.fontThickness)
        
        height = np.max(np.array((first_size[0][1], second_size[0][1], third_size[0][1], fourth_size[0][1])))
        width = np.max(np.array((first_size[0][0], second_size[0][0], third_size[0][0], fourth_size[0][0])))
        margin = int(0.4 * height)
        
        # read icons
        first_img = self.icons[first]
        second_img = self.icons[second]
        third_img = self.icons[third]
        fourth_img = self.icons[fourth]
        
        icon_width = icon_height = height
        first_img, second_img, third_img, fourth_img = [cv2.resize(img, (icon_width, icon_height))
                                                        for img in [first_img, second_img, third_img, fourth_img]]

        # draw object ID
        id_size = cv2.getTextSize(str(obj_id), self.fontFace, self.fontScale, self.fontThickness)
        id_height, id_width = id_size[0][1], id_size[0][0]
    
        top_left = (gt[1], gt[4] - id_height - 2 * margin)
        bottom_right = (gt[1] + id_width + 2 * margin, gt[4])
        cv2.rectangle(show_frame, top_left, bottom_right, (0, 0, 255), -1)
        
        bottom_left = (gt[1] + margin, gt[4] - margin)
        show_frame = cv2.putText(show_frame, str(obj_id), bottom_left, self.fontFace, self.fontScale, (255, 255, 255),
                                 self.fontThickness)

        grid = self.fancy_show_grid(show_frame, gt)
        
        if grid == 1:
            self.grid1(show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
                       first_img, second_img, third_img, fourth_img)
        elif grid == 2:
            self.grid2(show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
                       first_img, second_img, third_img, fourth_img)
        elif grid == 3:
            self.grid3(show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
                       first_img, second_img, third_img, fourth_img)
        elif grid == 4:
            self.grid4(show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
                       first_img, second_img, third_img, fourth_img)

        return show_frame

    def grid1(self, show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
              first_img, second_img, third_img, fourth_img):
        # draw background and bounding box of background
        top_left = (gt[1] - width - icon_width - 3 * margin, gt[4] - 4 * height - 5 * margin)
        bottom_right = (gt[1], gt[4])

        if all(element >= 0 for element in top_left):  # consider bounding box out of frame range
            cv2.rectangle(show_frame, top_left, bottom_right, self.color, -1)
            cv2.rectangle(show_frame, top_left, bottom_right, (0, 0, 255), self.thickness)
        
            # draw fourth label
            bottom_left = (gt[1] - width - margin, gt[4] - 3 * height - 4 * margin)
            show_frame = cv2.putText(show_frame, fourth, bottom_left, self.fontFace, self.fontScale,  self.fontColor,
                                     self.fontThickness)

            # draw third label
            bottom_left = (gt[1] - width - margin, gt[4] - 2 * height - 3 * margin)
            show_frame = cv2.putText(show_frame, third, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)
        
            # draw second label
            bottom_left = (gt[1] - width - margin, gt[4] - height - 2 * margin)
            show_frame = cv2.putText(show_frame, second, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)
        
            # draw first label
            bottom_left = (gt[1] - width - margin, gt[4] - margin)
            show_frame = cv2.putText(show_frame, first, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)
        
            # draw fourth icon
            rows = [gt[4] - 4 * height - 4 * margin, gt[4] - 3 * height - 4 * margin]
            cols = [gt[1] - width - icon_width - 2 * margin, gt[1] - width - 2 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = fourth_img
        
            # draw third icon
            rows = [gt[4] - 3 * height - 3 * margin, gt[4] - 2 * height - 3 * margin]
            cols = [gt[1] - width - icon_width - 2 * margin, gt[1] - width - 2 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = third_img

            # draw second icon
            rows = [gt[4] - 2 * height - 2 * margin, gt[4] - height - 2 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = second_img

            # draw first icon
            rows = [gt[4] - height - margin, gt[4] - margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = first_img

    def grid2(self, show_frame, gt, height, width, margin, icon_height, iconWidth, first, second, third, fourth,
              first_img, second_img, third_img, fourth_img):
        # draw background and bounding box of background
        top_left = (gt[3], gt[4] - 4 * height - 5 * margin)
        bottom_right = (gt[3] + width + iconWidth + 3 * margin, gt[4])

        if all(element >= 0 for element in top_left):  # consider bounding box out of frame range
            cv2.rectangle(show_frame, top_left, bottom_right, self.color, -1)
            cv2.rectangle(show_frame, top_left, bottom_right, (0, 0, 255), self.thickness)

            # draw fourth label
            bottom_left = (gt[3] + iconWidth + 2 * margin, gt[4] - 3 * height - 4 * margin)
            show_frame = cv2.putText(show_frame, fourth, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)
        
            # draw third label
            bottom_left = (gt[3] + iconWidth + 2 * margin, gt[4] - 2 * height - 3 * margin)
            show_frame = cv2.putText(show_frame, third, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)

            # draw second label
            bottom_left = (gt[3] + iconWidth + 2 * margin, gt[4] - height - 2 * margin)
            show_frame = cv2.putText(show_frame, second, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)

            # draw first label
            bottom_left = (gt[3] + iconWidth + 2 * margin, gt[4] - margin)
            show_frame = cv2.putText(show_frame, first, bottom_left, self.fontFace, self.fontScale, self.fontColor,
                                     self.fontThickness)

            # draw fourth icon
            rows = [gt[4] - 4 * height - 4 * margin, gt[4] - 3 * height - 4 * margin]
            cols = [gt[3] + margin, gt[3] + margin + iconWidth]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = fourth_img
        
            # draw third icon
            rows = [gt[4] - 3 * height - 3 * margin, gt[4] - 2 * height - 3 * margin]
            cols = [gt[3] + margin, gt[3] + iconWidth + margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = third_img

            # draw second icon
            rows = [gt[4] - 2 * height - 2 * margin, gt[4] - height - 2 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = second_img

            # draw first icon
            rows = [gt[4] - height - margin, gt[4] - margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = first_img

    def grid3(self, show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
              first_img, second_img, third_img, fourth_img):
        # draw background and bounding box of background
        top_left = (gt[3], gt[2])
        bottom_right = (gt[3] + icon_width + width + 3 * margin, gt[2] + 4 * height + 5 * margin)
        check_coordinate = (show_frame.shape[0] - bottom_right[1], show_frame.shape[1] - bottom_right[0])

        if all(element >= 0 for element in check_coordinate):  # consider bounding box out of frame range
            cv2.rectangle(show_frame, top_left, bottom_right, self.color, -1)
            cv2.rectangle(show_frame, top_left, bottom_right, (0, 0, 255), self.thickness)

            # draw fourth label
            bottom_left = (gt[3] + icon_width + 2 * margin, gt[2] + height + margin)
            show_frame = cv2.putText(show_frame, fourth, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw third label
            bottom_left = (gt[3] + icon_width + 2 * margin, gt[2] + 2 * height + 2 * margin)
            show_frame = cv2.putText(show_frame, third, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw second label
            bottom_left = (gt[3] + icon_width + 2 * margin, gt[2] + 3 * height + 3 * margin)
            show_frame = cv2.putText(show_frame, second, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw first label
            bottom_left = (gt[3] + icon_width + 2 * margin, gt[2] + 4 * height + 4 * margin)
            show_frame = cv2.putText(show_frame, first, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw fourth icon
            rows = [gt[2] + margin, gt[2] + icon_height + margin]
            cols = [gt[3] + margin, gt[3] + icon_width + margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = fourth_img

            # draw third icon
            rows = [gt[2] + icon_height + 2 * margin, gt[2] + 2 * icon_height + 2 * margin]
            cols = [gt[3] + margin, gt[3] + icon_width + margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = third_img

            # draw second icon
            rows = [gt[2] + 2 * icon_height + 3 * margin, gt[2] + 3 * icon_height + 3 * margin]
            cols = [gt[3] + margin, gt[3] + icon_width + margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = second_img

            # draw first icon
            rows = [gt[2] + 3 * icon_height + 4 * margin, gt[2] + 4 * icon_height + 4 * margin]
            cols = [gt[3] + margin, gt[3] + icon_width + margin]

            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = first_img

    def grid4(self, show_frame, gt, height, width, margin, icon_height, icon_width, first, second, third, fourth,
              first_img, second_img, third_img, fourth_img):
        # draw background and bounding box of background
        top_left = (gt[1] - width - icon_width - 3 * margin, gt[2])
        bottom_right = (gt[1], gt[2] + 4 * height + 5 * margin)
        check_coordinate = (show_frame.shape[0] - bottom_right[1], show_frame.shape[1] - bottom_right[0])

        if all(element >= 0 for element in check_coordinate):  # consider bounding box out of frame range
            cv2.rectangle(show_frame, top_left, bottom_right, self.color, -1)
            cv2.rectangle(show_frame, top_left, bottom_right, (0, 0, 255), self.thickness)

            # draw fourth label
            bottom_left = (gt[1] - width - margin, gt[2] + height + margin)
            show_frame = cv2.putText(show_frame, fourth, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw third label
            bottom_left = (gt[1] - width - margin, gt[2] + 2 * height + 2 * margin)
            show_frame = cv2.putText(show_frame, third, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw second label
            bottom_left = (gt[1] - width - margin, gt[2] + 3 * height + 3 * margin)
            show_frame = cv2.putText(show_frame, second, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw first label
            bottom_left = (gt[1] - width - margin, gt[2] + 4 * height + 4 * margin)
            show_frame = cv2.putText(show_frame, first, bottom_left, self.fontFace,
                                     self.fontScale, self.fontColor, self.fontThickness)

            # draw fourth icon
            rows = [gt[2] + margin, gt[2] + height + margin]
            cols = [gt[1] - width - icon_width - 2 * margin, gt[1] - width - 2 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = fourth_img

            # draw third icon
            rows = [gt[2] + height + 2 * margin, gt[2] + 2 * height + 2 * margin]
            cols = [gt[1] - width - icon_width - 2 * margin, gt[1] - width - 2 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = third_img

            # draw second icon
            rows = [gt[2] + 2 * height + 3 * margin, gt[2] + 3 * height + 3 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = second_img

            # draw first icon
            rows = [gt[2] + 3 * height + 4 * margin, gt[2] + 4 * height + 4 * margin]
            show_frame[rows[0]:rows[1], cols[0]:cols[1], :] = first_img
