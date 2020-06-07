from selenium import webdriver
from experience_points import ExperienceTable
from experience_points import ExperienceTableRow
from experience_points import ExperiencePoints

import re
import jsonpickle

def getWebsiteDriver():
    baseURL = "http://savanna.s15.xrea.com/dqmch_monster_lv99.shtml"
    #baseURL = "http://savanna.s15.xrea.com/dqmch_monster_001.shtml"
    driver = webdriver.Chrome()
    driver.get(baseURL)
    return driver

driver = getWebsiteDriver()

def scrape_experience_table(driver):
    title = driver.title
    monster_name = re.search('DQMCH(.*)成長特性', title).group(1)
    
    experience_rows = driver.find_elements_by_tag_name("tr")
    table = ExperienceTable()
    #the first row is the header so skip it
    for row in experience_rows[1:]:
        columns = row.find_elements_by_tag_name("td")
        level_reached = columns[0].text.replace("Lv","")
        if level_reached == "1":
            continue
        experience_required = columns[1].text
        row_hp = ExperienceTableRow(level_reached, experience_required, columns[2].text)
        table.hp.append(row_hp)
        row_mp = ExperienceTableRow(level_reached, experience_required, columns[3].text)
        table.mp.append(row_mp)
        row_attack = ExperienceTableRow(level_reached, experience_required, columns[4].text)
        table.attack.append(row_attack)
        row_defense = ExperienceTableRow(level_reached, experience_required, columns[5].text)
        table.defense.append(row_defense)
        row_speed = ExperienceTableRow(level_reached, experience_required, columns[6].text)
        table.speed.append(row_speed)
        row_intelligence = ExperienceTableRow(level_reached, experience_required, columns[7].text)
        table.intelligence.append(row_intelligence)
    
    return ExperiencePoints(monster_name, table)

all_monsters = []
url_rows = driver.find_elements_by_tag_name("tr")
for url_row_index in range(1, len(url_rows)):
    url_row = driver.find_elements_by_tag_name("tr")[url_row_index]
    url_tag = url_row.find_elements_by_tag_name("td")[0].find_element_by_tag_name("a")
    url_tag.click()
    monster_experience_points = scrape_experience_table(driver)
    all_monsters.append(monster_experience_points)
    driver.back()

def save_to_file(monsters, file_name):
    file = open(file_name, "w")
    json = jsonpickle.encode(monsters)
    file.write(json)
    file.close()

save_to_file(all_monsters, "monsters.txt")