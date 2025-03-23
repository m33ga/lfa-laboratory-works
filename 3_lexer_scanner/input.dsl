event juliusCaesarBirth {
    title = "Birth of Julius Caesar";
    date = 12-07-100 BCE ;
    importance = medium ;
}

event juliusCaesarDeath {
    title = "Assassination of Julius Caesar";
    date = 15-03-44 BCE ;
    importance = high ;
}

period romanRepublic {
    title = " Roman Republic ";
    start = 509 BCE ;
    end = 27 BCE ;
    importance = high ;
}

timeline romanHistory {
    title = "Roman History";
    juliusCaesarBirth , juliusCaesarDeath , romanRepublic;
}

main {
    for item in romanHistory {
        if ( item.year <= 0) {
            modify item {
                importance = high;
            }
        }
    }
    export romanHistory;
}


