import hashlib

def main():
    print("{0} encoded = {1}".format("a \b ",hashlib.md5("a \b ".encode("utf-8")).hexdigest()))
    print("{0} encoded = {1}".format("a ",hashlib.md5("a ".encode("utf-8")).hexdigest()))
    #print(bytes.fromhex("61200863").decode())
    #print("a\b ")
    #legitimateMessage = "As the Dean of Blakewell College, I have had the pleasure of knowing Cherise Rosetti for the last four years. She has been a tremendous asset to our school. I would like to take this opportunity to wholeheartedly recommend Cherise for your school's graduate program. I am confident that she will continue to succeed in her studies. She is a dedicated student and thus far her grades have been exemplary. In class, she has proven to be a take-charge person who is able to successfully develop plans and implement them. She has also assisted us in our admissions office. She has successfully demonstrated leadership ability by counseling new and prospective students. Her advice has been a great help to these students, many of whom have taken time to share their comments with me regarding her pleasant and encouraging attitude. For these reasons I highly recommend Cherise without reservation. Her ambition and abilities will truly be an asset to your establishment."

if __name__ == "__main__":
    main()