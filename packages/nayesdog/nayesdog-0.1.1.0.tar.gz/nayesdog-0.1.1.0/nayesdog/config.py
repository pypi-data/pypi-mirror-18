import os
import imp

default_config = """
'''Default configuration file generated by NayseDog'''
feeds_url_dict = {
    'NatureResearch': 'http://feeds.nature.com/NatureLatestResearch',
    'Arstechnica': 'http://feeds.arstechnica.com/arstechnica/science',
    'Science': 'http://www.sciencemag.org/rss/current.xml',
} 
word_counts_database_file = './tables.py.gz'
previous_session_database_file = '.previous_session'
maximal_number_of_entries_in_memory = 300
"""
user_config_file = "user_config.py"

def get_name_in_library(name,module_name="nayesdog"):
    library_location = imp.find_module(module_name)[1]
    return os.path.join(library_location, name)

def write_simple_config(file_name = user_config_file):
    with open(file_name,"w") as f:
        f.write(default_config)

server_address = ('127.0.0.1', 8081)
cssfile = get_name_in_library('css.css')
feeds_url_dict = {
    'NatureResearch': 'http://feeds.nature.com/NatureLatestResearch',
    'Arstechnica': 'http://feeds.arstechnica.com/arstechnica/science',
    'Science': 'http://www.sciencemag.org/rss/current.xml',
}
word_counts_database_file = './tables.py.gz'
stopwords_file = get_name_in_library('stopwords.txt')
previous_session_database_file = '.previous_session'
icons_folder = get_name_in_library("icons")
maximal_number_of_entries_in_memory = 300
list_of_user_parameters = [
"server_address",
"cssfile",
"feeds_url_dict",
"word_counts_database_file",
"stopwords_file",
"previous_session_database_file",
"maximal_number_of_entries_in_memory",
"icons_folder"]