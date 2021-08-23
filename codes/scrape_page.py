import pandas as pd
import json
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import locale
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.chrome.options import Options

def convert_datetime(value):
    locale.setlocale(locale.LC_TIME, "tr_TR")
    formats = ['%d %b %Y - %H:%M-','%d %b %Y - %H:%M', '%H:%M %d.%m.%Y', '%Y-%m-%d']
    result_format = '%d-%m-%Y'
    for dt_format in formats:
        try:
            dt_obj = datetime.strptime(value, dt_format)
            return dt_obj.strftime(result_format)
        except Exception as e:  # throws exception when format doesn't match
            pass
    return value  # let it be if it doesn't match


        

def get_milli_gazete(pages=None):
   
    main_url = "https://www.milligazete.com.tr"
    API_ENDPOINT = "https://www.milligazete.com.tr/arsiv/siyaset/"
    if pages is None:
        pages = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                17, 18, 19, 20, 21, 22, 23, 24, 25]
    post_urls = []        
    df = pd.DataFrame(columns=['Title','Text','Date','Brand']) 
    
    for page in pages:


        url = API_ENDPOINT + str(page)
        # Make GET request to the api endpoint
        try:
            response = requests.get(url, timeout = 20)
            
            # Create soup object
            soup = BeautifulSoup(response.text, 'html.parser')

            for post in soup.find_all('div',{'class':'post'}):
                post_url = post.find('a').get('href')
                post_url = main_url + post_url
                post_urls.append(post_url)
                print(post_url)
                try:   
                    response = requests.get(post_url, timeout=20)
                except:
                    pass
                
                soup = BeautifulSoup(response.text,'html.parser')
                title = soup.find('h1').get_text()
                
                text = soup.findAll('div',{'id':'main-text'})
                date = soup.find('span',{'class':'tarih'})
                if date is not None:
                    date = date.get_text()
                for x in text:
                    text2 = x.findAll('p').get_text()
                
                new_row = pd.DataFrame({'Title':[title], 'Text':[text2], 'Date':[date],'Brand':'Milli Gazete'})
                
                df = df.append(new_row, ignore_index= True)
                
                df['Date'] = df['Date'].apply(convert_datetime)
                print(new_row)
        except:
            pass
            
      
        
        
        
    return df


def get_sputnik(date=None):
    main_url = "https://tr.sputniknews.com"
    API_ENDPOINT = "https://tr.sputniknews.com/politika/"
    post_urls = []        
    df = pd.DataFrame(columns=['Title','Text','Date','Brand']) 
   
    years = ['2015','2016','2017','2018','2019','2020']
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24',
    '25','26','27','28','29','30','31']
    dates = []
    if date is None:
        for year in years:
            for month in months:
                for day in days:
                    dates.append(year+month+day)
    else:
        dates = date
    for date in dates:
        try:
           
            response = requests.get(API_ENDPOINT+date, timeout = 20)
            if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    soup = soup.find('div',{'class':'page_container m-relative root'}).find('div',{'class':'l-main m-oh'}).find('div',{'class':'l-wrap m-clear'})
                
                    soup = soup.find('div',{'class':'l-wrap m-oh l-wrapper'})
                    soup = soup.find('div',{'class':'l-maincolumn'}).find('div',{'class':'b-plainlist'})
                    soup = soup.find('ul',{'class':'b-plainlist__list'})
                    for post in soup.find_all('li',{'class':'b-plainlist__item'}):  
                        post_url = post.find('h1',{'class':'b-plainlist__title'})
                        post_url = post.find('a').get('href')
                        post_url = main_url + post_url
                        
                        post_urls.append(post_url)
                        print(post_url)
                            
                        try:   
                            response = requests.get(post_url, timeout=20)
                            
                            if response.status_code == 200:
                                
                                soup = BeautifulSoup(response.text,'html.parser')
                                soup = soup.find('div',{'class':'page_container m-relative root'})
                                
                                soup_header = soup.find('div',{'class':'l-wrap l-header'})
                                soup_header = soup_header.find('div',{'class':'b-header'})
                                
                                soup_header = soup_header.find('div',{'class':'b-article__header'})
                                title = soup_header.find('div',{'class':'b-article__header-title'})
                                title = soup_header.find('h1')
                                if title is not None:
                                    title = title.get_text()
                                
                                soup_text = soup.find('div',{'class':'l-main m-oh'}).find('div',{'class':'l-wrap m-clear'})
                                soup_text = soup_text.find('div',{'class':'l-maincolumn m-static'}).find('div',{'class':'b-article'})
                                
                                article_text = ''
                                text = soup.findAll('div',{'class':'b-article__text'})
                                for element in text:
                                    article_text += '\n' + ''.join(element.findAll(text = True))
                                
                                date = soup.find('time',{'class':'b-article__refs-date'}).get_text()
                                new_row = pd.DataFrame({'Title':[title], 'Text':[article_text], 'Date':[date],'Brand':'Sputnik'})
                                print(new_row)
                                df = df.append(new_row, ignore_index= True)
                                
                                df['Date'] = df['Date'].apply(convert_datetime)
                                print(new_row)
                        except:
                            pass
                  
        except: 
            pass
        
    
    return df   

def get_sabah(date = None):
    main_url = "https://www.sabah.com.tr"
    API_ENDPOINT = "https://www.sabah.com.tr/timeline/"
    post_urls = []        
    df = pd.DataFrame(columns=['Title','Text','Date','Brand'])
    years = ['2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24',
    '25','26','27','28','29','30','31']
    dates = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver2 = webdriver.Chrome(options=options)
    if date is None:
        
        for year in years:
            for month in months:
                for day in days:
                    dates.append('/'+year+'/'+month+'/'+day)
    else:
        dates = date
    
    for date in dates:
        
        driver.get(API_ENDPOINT+date+'?c=gundem')
        news_list = driver.find_elements_by_class_name('box')
        for element in news_list:
            try:
               
                post_url = element.find_element_by_class_name('innerItem').find_element_by_tag_name('a').get_attribute('href')
                post_urls.append(post_url)
                title = element.find_element_by_class_name('innerItem').find_element_by_tag_name('strong').text
                print(title)
                print(post_url)
                try:
                    driver2.get(post_url)
                    article_text = driver2.find_element_by_class_name('detailText').text
                    print(article_text)
                except NoSuchElementException:
                    article_text = ''

                try:
                    article_text = driver2.find_element_by_class_name('newsBox').text
                    print(article_text)
                except NoSuchElementException:
                    article_text = ''
               
                print(date)

                if article_text is not '':

                    new_row = pd.DataFrame({'Title':[title], 'Text':[article_text], 'Date':[date],'Brand':'Sabah'})

                    df = df.append(new_row, ignore_index= True)

                    df['Date'] = df['Date'].apply(convert_datetime)
                    print(new_row)
            except:
                pass

    

        
    return df

def get_hurriyet(date = None):

    main_url = "https://www.hurriyet.com.tr/arama/#/?where=/&how=Article&isDetail=false"
    post_urls = []
    df = pd.DataFrame(columns=['Title','Text','Date','Brand'])
    driver3 = webdriver.Chrome(executable_path=r'C:\Users\casper\Downloads\chromedriver.exe')
    for i in range (1,251):
        print(main_url+"&page="+str(i))
        driver3.get(main_url+"&page="+str(i))
        time.sleep(5)
        category = driver3.find_elements_by_class_name('hs-cnncc-category')
       
        
        for element in category:
            
           
            if element.text == 'Gündem':

                post_url = element.find_element_by_tag_name('a').get_attribute('href')
                post_urls.append(post_url)
                print(post_url)


   
   
    for post in post_urls:
    
        driver3.get('http://www.hurriyet.com.tr/gundem/son-dakika-haberler-hurriyet-yazarlari-yorumladi-tarihi-an-bu-daha-baslangic-41592798')
        
        title = driver3.find_element_by_class_name('rhd-article-title')
        if title is not None:
            title = title.text
        article_text = driver3.find_element_by_class_name('rhd-all-article-detail ')
        if article_text is not None:
            
            article_text =article_text.text
        date = driver3.find_element_by_tag_name('time').text
       

        new_row = pd.DataFrame({'Title':[title], 'Text':[article_text], 'Date':[date],'Brand':'Hürriyet'})
        
        df = df.append(new_row, ignore_index= True)

        df['Date'] = df['Date'].apply(convert_datetime)
        print(new_row)
    return df

def get_hurriyet_daily(date = None):

    main_url = "https://www.hurriyet.com.tr/gundem/"
    url = "https://www.hurriyet.com.tr"
    post_urls = []
    df = pd.DataFrame(columns=['Title','Text','Date','Brand'])
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(main_url)
    news_list = driver.find_elements_by_class_name('main-newslist-item')
    for element in news_list:
      
        post_url = element.find_element_by_tag_name('a')
        
        post_urls.append(post_url.get_attribute('href'))
    print(post_urls)
    for post in post_urls:

        driver.get(post)
        try:

            title = driver.find_element_by_tag_name('h1').text
        except NoSuchElementException:
            title = ''
        try:
            article_text = driver.find_element_by_class_name('rhd-sticky-limit').text
        except NoSuchElementException:
            article_text = ''
        try:
            date = driver.find_element_by_tag_name('time').text
       except NoSuchElementException:
           date = ''

        new_row = pd.DataFrame({'Title':[title], 'Text':[article_text], 'Date':[date],'Brand':'Hürriyet'})
        
        df = df.append(new_row, ignore_index= True)

        df['Date'] = df['Date'].apply(convert_datetime)
        print(new_row)
    
    return df



if __name__ == '__main__':
    queue_url = "https://sqs.eu-west-1.amazonaws.com/724062815624/run-queue"

    sqs = boto3.client('sqs')
    
    message_bodies = []
    while 1:
        
        try:
            response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
            message = response['Messages'][0]
            message_bodies.append(message)
            message.delete()
        
        except:
            print('Empty Queue')
        if message:
            #sputnik_yesterday = datetime.today() - datetime.timedelta(1)
            #sputnik_yesterday = sputnik_yesterday.strftime('%Y%m%d')
            #sabah_today = datetime.today().strftime('%Y/%m/%d')
            #df_milligazete = get_milli_gazete()
            #df_milligazete =  get_milli_gazete([1,2,3])#get last 3 pages
            #df_sputnik = get_sputnik()
            #df_sputnik = get_sputnik(sputnik_yesterday)
            #df_sabah = get_sabah()
            df_hurriyet = get_hurriyet()
            #df_sabah =get_sabah(sabah_today)
            #frames = [df_milligazete,df_sputnik,df_sabah]
            #df = pd.concat(frames)
            #df['Timestamp '] = datetime.now()
            print(df_hurriyet)
            df_hurriyet= df_hurriyet.astype({'Date':str,'Timestamp':str})
            df_hurriyet.to_csv('data.csv',encoding='utf-8')
            s3 = boto3.client('s3')
            wr.s3.to_parquet(
            df=df_hurriyet,
            path="s3://pols-project-bucket/dataset/results.parquet",
            dataset=True,
            database = 'db',
            table = 'news_table'

            )


            queue_url2 = "https://sqs.eu-west-1.amazonaws.com/724062815624/stop-queue"
            response = sqs.send_message(
            QueueUrl=queue_url2,
            DelaySeconds=10,
            MessageBody=(
                'stop instance '
               
            )
        )

            print(response['MessageId'])

        
            

   


   
    
    
