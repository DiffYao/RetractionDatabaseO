from re import split
from selenium import webdriver
import time

def run(driver, begin_date, end_date):
    
    #id : txtOriginalDateFrom
    from_date = driver.find_element_by_name('txtOriginalDateFrom')
    #id : txtOriginalDateTo
    to_date = driver.find_element_by_name('txtOriginalDateTo')  

    from_date.clear()
    to_date.clear()
    
    from_date.send_keys(begin_date)
    to_date.send_keys(end_date)
    


    #id: btnSearch
    search = driver.find_element_by_name('btnSearch')
    search.click()


    # table data
    table_item = driver.find_elements_by_xpath('//*[@id="grdRetraction"]/tbody/tr')
    # table = driver.find_element_by_xpath('//*[@id="grdRetraction"]/tbody/tr[2]/td[2]/a');

    root_path = '//*[@id="grdRetraction"]/tbody/tr'

    try:
        
        for i in range(2, len(table_item)):
            temp_str = ''
            temp_list = []
            son_path = root_path + '['+ str(i) + ']/td'
            son_path_td =  driver.find_elements_by_xpath(son_path)
            
            son_path_Title = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rTitleNotIE"]')
            son_path_Subject = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rSubject"]')
            son_path_Journal = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rJournal"]'+'//*'+'[@class="rJournal"]')
            son_path_Publish = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rPublisher"]')
            son_path_Institution = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rInstitution"]')
            son_path_Reason = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rReason"]')
            son_path_AuthorLink = driver.find_elements_by_xpath(son_path+'//*'+'[@class="authorLink"]')
            son_path_Nature = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rNature"]')
            son_path_Paywalled = driver.find_elements_by_xpath(son_path+'//*'+'[@class="rPaywalled"]')
            temp_list.append(son_path_Title)
            temp_list.append(son_path_Subject)
            temp_list.append(son_path_Publish)
            temp_list.append(son_path_Institution)
            temp_list.append(son_path_Reason)
            temp_list.append(son_path_AuthorLink)
            temp_list.append(son_path_Nature)
            temp_list.append(son_path_Paywalled)
            for l in temp_list:
                for k in l:
                    temp_str += (k.text + '&')
                temp_str += '$'
            for k in son_path_Journal:
                stri = k.text
                temp_str += (stri + '&')
            temp_str += '$'
            #original paper date 
            if (4 < len(son_path_td)): 
                ori_date = son_path_td[4]
                temp_str += (ori_date.text[0:10])
            temp_str += '$'
        
            #retraction paper date 
            if (5 < len(son_path_td)): 
                retra_date = son_path_td[5]
                temp_str += (retra_date.text[0:10])
            temp_str += '$'
            
            #countrys
            if (7 < len(son_path_td)):
                countrys = son_path_td[7]
                split_str = countrys.text.split('\n')
                for s in split_str:
                    if (s != 'Yes' and s != 'No'):
                        temp_str += (s + '&')
            
            #f.write(begin_date + ' ' + str(i) + ' ' + temp_str+'\n')
            f.write(temp_str+'\n')
            
        
    except Exception as e:
        print('exception ' + str(e))
    finally:
        print('-----------------')
        #print(table_item[0].text)    

if __name__ == "__main__":
    url = 'http://retractiondatabase.org'
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get(url)
    f = open('run.log', 'w+', encoding='utf-8')
    for j in range(0, 21):
        for i in range(1, 12):
            start_Data = str(i) + '/01/' + str(2000 + j)
            end_Data = str(i) + '/15/' + str(2000+j)
            print(start_Data)
            run(driver, start_Data, end_Data)
            start_Data = str(i) + '/15/' + str(2000+j)
            end_Data = str((i + 1)) + '/01/' + str(2000 + j)
            print(start_Data)
            run(driver, start_Data, end_Data)
        start_Data = '12' + '/01/' + str(2000 + j)
        end_Data = '12' + '/15/' + str(2000+j)
        print(start_Data)
        run(driver, start_Data, end_Data)
        start_Data = '12' + '/15/' + str(2000+j)
        end_Data = '01' + '/01/' + str(2000 + j + 1)
        print(start_Data)
        run(driver, start_Data, end_Data)
    time.sleep(1)
    f.close()
    driver.quit()
    pass