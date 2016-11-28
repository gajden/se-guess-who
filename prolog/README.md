Podłączenie silnika prologowego do wybornie prymitywnego gui:

- przygotować klasę, która implementuje interfejs 
    z search_engine_interface.py,
    get_question() powinno zwracać string z początkowym pytaniem 
            dla osoby
            
    answer_yes() wywołanie oznacza odpowiedź 'tak' na ostatnie zadane 
            pytanie, powinno zwracać dwie wartości: 
            string - jesli osoba nie została odgadnięta zwraca kolejne
                    pytanie, w przeciwnym wypadku jest to nazwisko
                    odgadniętej osoby
            boolean - True, jeśli osoba została odgadnięta, False
                    w przeciwnym wypadku
                    
    answer_no() wywołanie oznacza odpowiedź 'nie' na ostatnie
            zadane pytanie, zwraca wartości analogiczne dla answer_yes()
    
- W linijce 84 w app.py podmienić SearchStub() na swoją klasę

- To wszystko, dziękuję za uwagę
