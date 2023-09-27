#WEBSCRAPPING TASK
# =============================================================================
# www.acemicromatic.net
#Host
#Error
# =============================================================================


#successfully completed scraping the details of all products except vertical machining centers due to bad gateway error.
#pending work due to the website error:
    #extracting details from vertical machining centers
    #storing the scraped data to a pandas data frame 
    #saving it as an excel file
    
    

#importing libraries
import requests
from bs4 import BeautifulSoup
#=============================================maincategory========================================================


#downloading the html code from the first_page
url='https://www.acemicromatic.net/product_cat/milling/'
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"}
html=requests.get(url,headers=headers)
#setting the webscraper/creating the spoon
s=BeautifulSoup(html.content,'html.parser')#beautiful soup object
#list of machines
machine_class=s.find_all(class_='content slide')
machine_name=[]
for each_machine in machine_class:
    machine_name.append(each_machine.find('h4').text)
print(machine_name)
#output:['Drill Tap Machining Centers ', 'Vertical Machining Centers ', 'Twin Spindle VMC ', '5 Axes VMC ', 'Special VMC ', 'Double Column ', 'Horizontal Machining Centers ']]


#=============================================subcategory========================================================


#creating the beautifulsoup object for finding the sub category of each products
token=[]
for element in machine_name:
    count=len(element.split())-1
    token.append(element.rstrip().replace(' ', '-',count))    
token[2]='Twin-Spindle-VMC-geminis'
print(token)

machine_type1_names=[]
for i in range(len(token)):
    url1='https://www.acemicromatic.net/product_cat/'+token[i]+'/'
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"}
    html1=requests.get(url1,headers=headers)
    s1=BeautifulSoup(html1.content,'html.parser')
    #list of the types per machine
    machine_type1=s1.find_all(class_='content')
    for element in machine_type1[1:]:
        machine_type1_names.append(element.find('h4').text)        
    # extracting the details of each machine_type_name
    token1=[]
    for element in machine_type1_names:
         count=len(element.split())-1
         token1.append(element.rstrip().replace(' ', '-',count).replace('.','')) 
         elements_to_remove=['Small','Medium','Large','V-Series','Heavy-Duty']
         for element in elements_to_remove:
           if element in token1:
              token1.remove(element)



#========================================scraping the details========================================================


main_list=[]    
for i in range(len(token1)):
        url2='https://www.acemicromatic.net/aceproduct/'+token1[i]+'/#specification'
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"}
        html2=requests.get(url2,headers=headers)
        s2=BeautifulSoup(html2.content,'html.parser')
        list=[]     
#       ------PARAM1-----------------
        if(s2.find('a',text='Milling').text is None):
            list.append('Milling')
        else:
            list.append(s2.find('a',text='Milling').text)
#       -----PARAM2------------------   
        list.append(s2.find('span',class_='type').text)
        list.append(s2.find('h3').text)
#       ------x,y,z-------------------        
        if(s2.find('table') is None):
            for i in range(0,3):
             list.append("Data Not Found")
             
        elif(s2.find('table').find('tbody').find('tr',class_='hide_row hide_2').find_next('td').text == 'TRAVELS (X/Y/Z)'):
            x=s2.find('table').find('tbody').find('tr',class_='hide_row hide_2').find('td',text='mm').find_next('td').text.replace("\n","").replace(" ","").split("/")
            for item in x:
                list.append(int(item))
        
        elif(s2.find('table').find('tbody').find_all('tr',class_='hide_row hide_2')[1].find('td').text!='Y - AXIS TRAVEL'):
                y=s2.find('table').find('tbody').find('tr',class_='hide_row hide_2').find('td',text='mm').find_next('td').text.replace("\n","").replace(" ","").split("/")
                for item in y:
                    list.append(int(item))
        else:    
            x=s2.find('table').find('tbody').find_all('tr',class_='hide_row hide_2')
            for i in range(0,3):
                travel=x[i].find('td',text='mm').find_next('td').text.replace("\n","").replace(" ","").split("/")
                for item in travel:
                       list.append(int(item))   
        #print(list)
        main_list.append(list)


# Example code for saving to Excel:
# import pandas as pd
# df = pd.DataFrame(main_list,headers=[param1,param2,model_name,x_travel,y_travel,z_travel_std])
# df.to_excel('machine_data_milling.xlsx',index=False)

#========================================special-case========================================================


# =============================================================================
#         vmc=['430-v','mcv-300','mcv-350','super-winner','mcv-400','mcv-400-f','mcv-400-xl',
#             'mcv-450','mcv-450-xl','acer','acer-xl','mcv-550-l','mcv-650','mcv-700','mcv-700-n',
#             'mcv-700-n-l','mcv-800','540v','730v','740v','740v-dm','850v','1060v','1260v','1580v',
#             ]
#         
# =============================================================================
