from bs4 import BeautifulSoup
import requests
import re
import os.path
#import time


# function to determine if text is Chinese or not
def is_chinese(text):
        non_chinese = 0
        total = 0

        for ch in text:
                if ord(ch) < 0x4e00 or ord(ch) > 0x9fff:
                        non_chinese += 1
                total += 1

        if total == 0:
                return False

        if ((non_chinese / total) > 0.8):
                return False
        else:
                return True

###

r  = requests.get("http://www.slow-chinese.com/podcast/")

data = r.text

soup = BeautifulSoup(data)

# find all the h2s in the archive page because they contain links to the podcasts
for h2s in soup.find_all('h2'):

        # mp3 links file
        #mp3_list_file = open("mp3s.txt", "w")
        #mp3_list_file.close()        
        mp3_links_list = []
        
        # find the link to each episode in the h2
        for link in h2s.find_all('a'):
                # start processing this episode
                episode_url = link.get('href')
                episode_name = episode_url[episode_url[:-2].rfind('/')+1:-1]
                output_file_name = episode_name + ".txt"

                chinese_paragraph_count = 0

                print("Processing " + episode_url + "...")

                if not os.path.isfile(output_file_name):
                        
                        r = requests.get(episode_url)
                        data = r.text
                        soup = BeautifulSoup(data)

                        # get mp3 link
                        for a in soup.find_all('a',href=re.compile('http.*\.mp3')):
                                mp3_link = a.get('href')
                                if mp3_link not in mp3_links_list:
                                        print(">> mp3: " + mp3_link)
                                        mp3_links_list.append(mp3_link)
                                        mp3_list_file = open("mp3s.txt", "a")
                                        mp3_list_file.write(mp3_link + "\n")
                                        mp3_list_file.close()

                        # get all text and go looking for the paragraph after <p class="powerpress_embed_box">
                        powerpress_embed_box = soup.find("p", class_="powerpress_embed_box")
                        ##lesson_text_paragraph = powerpress_embed_box.find_next('p')

                        lesson_text_file = open(output_file_name, "w")

                        # 2 lines here are a dirty hack to get around a formatting error in a couple of posts
                        # they accidentally added an empty p to the html outside the div
                        ##lesson_text_file.write(lesson_text_paragraph.text)
                        ##lesson_text_paragraph = lesson_text_paragraph.find_next('p')

                        #print(lesson_text_paragraph.next_sibling)


                        # loop through lesson text p tags
                        # (newer lessons‘ Chinese text is in <div id="-0">)
                        # (earlier lessons end in <p>&nbsp;</p>)
                        # ***(other lessons end in next <div>)


                        ###
                        ### REVISE THIS
                        ### Try getting list of all p tags then looping through them using for in loop?
                        #lesson_paragraphs = powerpress_embed_box.find_all_next('p', text=True)
                        lesson_paragraphs = powerpress_embed_box.find_all_next('p')

                        for paragraph in lesson_paragraphs:
                                paragraph_string = paragraph.text
                                if (is_chinese(paragraph_string) and (paragraph.find_parent("section", id="comments") is None)):
                                        lesson_text_file.write(paragraph_string + "\n\n")
                                        chinese_paragraph_count += 1

                        lesson_text_file.close()

                        print(str(chinese_paragraph_count) + " paragraphs of lesson text saved to " + output_file_name)


                        ### check 1st char/5th char/10th/20th char for Chinese language？
                        ### + check if the p tags belong to the body OR div -0 id?
                        ###


                        #while ((lesson_text_paragraph.text != "&nbsp;") and ((lesson_text_paragraph.parent['id'] == "-0")):
                                #print(lesson_text_paragraph.parent['id'])
                                #print(lesson_text_paragraph.text)
                        #        lesson_text_file.write("\n\n" + lesson_text_paragraph.text)
                                #print(lesson_text_paragraph.prettify())
                        #        lesson_text_paragraph = lesson_text_paragraph.find_next('p')

                        ###        if (lesson_text_paragraph.next_sibling.next_sibling.name != u"div"):
                        ###                break

                        

                else:
                        print(output_file_name + " exists, skipping...")

                print("\n* * * * *\n")



                #text_full = soup.find_all("p", id="", title="")
                #for paragraph in text_full:
                #        print(repr(paragraph.string))

        
