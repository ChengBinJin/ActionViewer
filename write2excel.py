import numpy as np
import xlsxwriter


class Writer():
    def __init__(self):

        # Create a workbook and add a worksheet.
        self.workbook = xlsxwriter.Workbook('Statistics.xlsx')

        self.worksheet = self.workbook.add_worksheet()
        self.xlsFormat = self.workbook.add_format()
        self.xlsFormat.set_align('center')
        self.xlsFormat.set_valign('vcenter')
        
        self.write_keywords()

    def __del__(self):
        self.workbook.close()        
        
    def write_keywords(self):
        # write head filer
        self.worksheet.write(0, 0, 'Number', self.xlsFormat)  # index of the video
        self.worksheet.write(0, 1, 'video_name', self.xlsFormat)   # video name
        
        self.worksheet.write(0, 2, 'Num. of people', self.xlsFormat)  # number of people
        
        self.worksheet.write(0, 3, 'Time', self.xlsFormat)  # video time
        
        self.worksheet.write(0, 4, '0:Sitting', self.xlsFormat)
        self.worksheet.write(0, 5, '1:Standing', self.xlsFormat)
        self.worksheet.write(0, 6, '2:Lying', self.xlsFormat)
        
        self.worksheet.write(0, 7, '0:Stationary', self.xlsFormat)
        self.worksheet.write(0, 8, '1:Waling', self.xlsFormat)
        self.worksheet.write(0, 9, '2:Running', self.xlsFormat)
        self.worksheet.write(0, 10, '3:Bicycling', self.xlsFormat)
        self.worksheet.write(0, 11, '4:Falling', self.xlsFormat)
        
        self.worksheet.write(0, 12, '0:Nothing', self.xlsFormat)
        self.worksheet.write(0, 13, '1:Texting', self.xlsFormat)
        self.worksheet.write(0, 14, '2:Smoking', self.xlsFormat)
        self.worksheet.write(0, 15, '3:Phoning', self.xlsFormat)
        self.worksheet.write(0, 16, '4:Others', self.xlsFormat)
        
        self.worksheet.write(0, 17, '0:Nothing', self.xlsFormat)
        self.worksheet.write(0, 18, '1:Littering', self.xlsFormat)
    
    def write2excel(self, path, video_id, gt, video_time):
        statistics = dict()
        
        statistics['video_name'] = path[-8:]

        gt = np.asarray(gt)
        statistics['num_of_people'] = np.max(gt, axis=0)[6]

        statistics['num_of_sitting'] = np.sum(gt[:, 7] == 0)
        statistics['num_of_standing'] = np.sum(gt[:, 7] == 1)
        statistics['num_of_lying'] = np.sum(gt[:, 7] == 2)
        
        statistics['num_of_stationary'] = np.sum(gt[:, 8] == 0)
        statistics['num_of_walking'] = np.sum(gt[:, 8] == 1)
        statistics['num_of_running'] = np.sum(gt[:, 8] == 2)
        statistics['num_of_bicycling'] = np.sum(gt[:, 8] == 3)
        statistics['num_of_falling'] = np.sum(gt[:, 8] == 4)
        
        statistics['num_of_nothing_3'] = np.sum(gt[:, 9] == 0)
        statistics['num_of_texting'] = np.sum(gt[:, 9] == 1)
        statistics['num_of_smoking'] = np.sum(gt[:, 9] == 2)
        statistics['num_of_phoning'] = np.sum(gt[:, 9] == 3)
        statistics['num_of_others'] = np.sum(gt[:, 9] == 9)
        
        statistics['num_of_nothing_4'] = np.sum(gt[:, 10] == 0)
        statistics['num_of_littering'] = np.sum(gt[:, 10] == 1)
           
        print("Name: ", statistics['video_name'])
        # print("People: ", statistics['num_of_people'])
        
        # print("Sitting: ", statistics['num_of_sitting'])
        # print("Standing: ", statistics['num_of_standing'])
        # print("Lying: ", statistics['num_of_lying'])
        
        # print("Stationary: ", statistics['num_of_stationary'])
        # print("Walking: ", statistics['num_of_walking'])
        # print("Running: ", statistics['num_of_running'])
        # print("Bicycling: ", statistics['num_of_bicycling'])
        # print("Falling: ", statistics['num_of_falling'])
        
        # print("Nothing: ", statistics['num_of_nothing_3'])
        # print("Texting: ", statistics['num_of_texting'])
        # print("Smoking: ", statistics['num_of_smoking'])
        # print("Phoning: ", statistics['num_of_phoning'])
        # print("Others: ", statistics['num_of_others'])
        
        # print("Nothing: ", statistics['num_of_nothing_4'])
        # print("Littering: ", statistics['num_of_littering'])
    
        # print("Video ID: ", video_id)
        # write statistics information
        self.worksheet.write(video_id, 0, video_id, self.xlsFormat)  # index of the video
        self.worksheet.write(video_id, 1, statistics['video_name'], self.xlsFormat)   # video name
        
        self.worksheet.write(video_id, 2, statistics['num_of_people'], self.xlsFormat)  # number of people
        
        # convert second to format time
        self.worksheet.write(video_id, 3, self.convert2format(video_time), self.xlsFormat)  # video time
        
        self.worksheet.write(video_id, 4, statistics['num_of_sitting'], self.xlsFormat)
        self.worksheet.write(video_id, 5, statistics['num_of_standing'], self.xlsFormat)
        self.worksheet.write(video_id, 6, statistics['num_of_lying'], self.xlsFormat)
        
        self.worksheet.write(video_id, 7, statistics['num_of_stationary'], self.xlsFormat)
        self.worksheet.write(video_id, 8, statistics['num_of_walking'], self.xlsFormat)
        self.worksheet.write(video_id, 9, statistics['num_of_running'], self.xlsFormat)
        self.worksheet.write(video_id, 10, statistics['num_of_bicycling'], self.xlsFormat)
        self.worksheet.write(video_id, 11, statistics['num_of_falling'], self.xlsFormat)
        
        self.worksheet.write(video_id, 12, statistics['num_of_nothing_3'], self.xlsFormat)
        self.worksheet.write(video_id, 13, statistics['num_of_texting'], self.xlsFormat)
        self.worksheet.write(video_id, 14, statistics['num_of_smoking'], self.xlsFormat)
        self.worksheet.write(video_id, 15, statistics['num_of_phoning'], self.xlsFormat)
        self.worksheet.write(video_id, 16, statistics['num_of_others'], self.xlsFormat)
        
        self.worksheet.write(video_id, 17, statistics['num_of_nothing_4'], self.xlsFormat)
        self.worksheet.write(video_id, 18, statistics['num_of_littering'], self.xlsFormat)
        
    @staticmethod
    def convert2format(time):
        hour = time // 60 // 60
        minute = time // 60
        second = time % 60
        
        format_time = str(hour) + ":" + str(minute).zfill(2) + ":" + str(second).zfill(2)
        return format_time

