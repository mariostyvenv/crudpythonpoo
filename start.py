import subprocess as sp
from models.Word import Word
from terminaltables import AsciiTable


def main():
    word = Word()
    if word.startDatabase():

        while True:

            sp.call('cls',shell=True)
            sel = input("\n\n(1) See all the words\n(2) See the words learned\n(3) See the words to learn\n(4) See reviews\n(5) Start learning\n(6) Start review\n(7) Reset database\n(8) Exit\n\n >> ")

            if sel == '1':
                result = word.getAllResult()
                header = ('ID','WORD','NO LEARN', 'REVIEW', 'LEARNED', 'SENTENCE')
                result.insert(0, header)
                table = AsciiTable(result)
                print(table.table)
                input()

            elif sel == '2':
                result = word.getLearned()
                header = ('ID','WORD','SENTENCE')
                result.insert(0, header)
                table = AsciiTable(result)
                print(table.table)
                input()

            elif sel == '3':
                result = word.getNotLearned()
                header = ('ID','WORD')
                result.insert(0, header)
                table = AsciiTable(result)
                print(table.table)
                input()

            elif sel == '4':

                result = word.getReview()
                header = ('ID','WORD', 'SENTENCE')
                result.insert(0, header)
                table = AsciiTable(result)
                print(table.table)
                input()

            elif sel == '5':

                result = word.startLearn()
                for w in result:
                    res = [('{}'.format(w[0]), '{}'.format(w[1]))]
                    table = AsciiTable(res)
                    print(table.table)
                    sentence = input("\n\nInsert sentence: ")

                    if word.saveSentence(w[0], sentence):
                        con = input("continue? (y/n): ")
                        if con.lower() == 'n':
                            break
                    else:
                        print("Error al momento de guardar la oracion")
            

            elif sel == '6':

                result = word.getReview()
                if len(result) != 0:

                    for w in result:
                        res = [('{}'.format(w[0]), '{}'.format(w[1]))]
                        table = AsciiTable(res)
                        print(table.table)
                        sentence = input("\n\nInsert sentence: ")

                        if word.confirmReview(w[0], sentence):

                            con = input("continue? (y/n): ")

                            if con.lower() == 'n':
                                break

                        else:
                            print("Error al momento de guardar la oracion")
                else:
                    print("No results were found to practice")

            elif sel == '7':

                if word.resetDatabase():
                    print("Database reset successful")
                    input()
                

            elif sel == '8':
                print("Bye!")
                break
            else:
                input("¡Selección incorrecta!")

if __name__ == "__main__":
    main()
