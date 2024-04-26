from imdb import Cinemagoer
import pandas as pd

ia = Cinemagoer()
df3 = pd.read_csv("movie_data.csv")

def narrow(index, maturity, director_star_lm):
    maturity = maturity.lower().strip()
    director_star_lm = [name.lower().strip() for name in director_star_lm]  

    if df3.iloc[index, 8].lower().strip() != maturity and maturity != "no":
        return False

    
    movie_director_star_list = df3.iloc[index, 9].lower().strip().split(', ') + df3.iloc[index, 10].lower().strip().split(', ')

    
    for name in director_star_lm:
        if name in movie_director_star_list:
            return True

    return False



'''
index = 0  # Replace with the index of the movie you're interested in
maturity = "PG-13"
director_star = "Christopher Nolan, Leonardo DiCaprio"

result = narrow(index, maturity, director_star)
print(result)
'''