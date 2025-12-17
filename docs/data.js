export const rankings = [
  {
    sport: 'Football',
    items: [
      { rank: 1, team: 'Linganore' },
      { rank: 2, team: 'Oakdale' },
      { rank: 3, team: 'Middletown' },
      { rank: 4, team: 'Urbana' },
    ]
  },
  {
    sport: 'Boys Soccer',
    items: [
      { rank: 1, team: 'Tuscarora' },
      { rank: 2, team: 'Urbana' },
      { rank: 3, team: 'Linganore' },
      { rank: 4, team: 'Brunswick' },
    ]
  },
  {
    sport: 'Girls Flag Football',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Linganore' },
      { rank: 3, team: 'Frederick' },
      { rank: 4, team: 'Thomas Johnson' },
    ]
  },
  {
    sport: 'Girls Soccer',
    items: [
      { rank: 1, team: 'Oakdale' },
      { rank: 2, team: 'Linganore' },
      { rank: 3, team: 'Brunswick' },
      { rank: 4, team: 'Middletown' },
    ]
  },
  {
    sport: 'Volleyball',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Tuscarora' },
      { rank: 3, team: 'Oakdale' },
      { rank: 4, team: 'Maryland School for the Deaf' },
    ]
  },
  {
    sport: 'Field Hockey',
    items: [
      { rank: 1, team: 'Linganore' },
      { rank: 2, team: 'Urbana' },
      { rank: 3, team: 'Walkersville' },
      { rank: 4, team: 'Oakdale' },
    ]
  },
  {
    sport: 'Boys Cross Country',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Thomas Johnson' },
      { rank: 3, team: 'Brunswick' },
      { rank: 4, team: 'Oakdale' },
    ]
  },
  {
    sport: 'Girls Cross Country',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Thomas Johnson' },
      { rank: 3, team: 'Frederick' },
      { rank: 4, team: 'Tuscarora' },
    ]
  },
  {
    sport: 'Golf',
    items: [
      { rank: 1, team: 'Linganore' },
      { rank: 2, team: 'Middletown' },
      { rank: 3, team: 'Oakdale' },
    ]
  },
];

export const sportsData = [
  {
    id: 'football',
    name: 'Football',
    standings: [
      {
        name: 'FCPS',
        headers: ['W', 'L', 'PF', 'PA'],
        rows: [
          { team: 'Linganore', w: 13, l: 0, pf: 578, pa: 137 },
          { team: 'Oakdale', w: 10, l: 3, pf: 478, pa: 221 },
          { team: 'Middletown', w: 8, l: 3, pf: 371, pa: 150 },
          { team: 'Urbana', w: 7, l: 5, pf: 348, pa: 234 },
          { team: 'Walkersville', w: 7, l: 5, pf: 377, pa: 292 },
          { team: 'Frederick', w: 5, l: 6, pf: 318, pa: 283 },
          { team: 'Brunswick', w: 2, l: 8, pf: 152, pa: 334 },
          { team: 'Thomas Johnson', w: 2, l: 8, pf: 213, pa: 442 },
          { team: 'Tuscarora', w: 2, l: 8, pf: 154, pa: 425 },
          { team: 'Catoctin', w: 1, l: 9, pf: 72, pa: 301 },
        ]
      },
      {
        name: 'Other Schools',
        headers: ['W', 'L', 'PF', 'PA'],
        rows: [
          { team: 'Maryland School for the Deaf', w: 9, l: 3, pf: 418, pa: 127 },
          { team: "St. John's Catholic Prep", w: 0, l: 10, pf: 92, pa: 333 },
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Rushing',
        headers: [
            { key: 'att', label: 'Att' }, 
            { key: 'yds', label: 'Yds' }, 
            { key: 'avg', label: 'Avg' }, 
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Bradly Matthews', school: 'Linganore', att: 246, yds: '2,124', avg: 8.63, td: 41 },
          { player: 'Colton Amoriell', school: 'Walkersville', att: 235, yds: '1,765', avg: 7.5, td: 21 },
          { player: 'Mark Gwynn III', school: 'Maryland School for the Deaf', att: 103, yds: '1,095', avg: 10.63, td: 14 },
          { player: 'Alex Rodriguez', school: 'Oakdale', att: 134, yds: '1,042', avg: 7.77, td: 16 },
          { player: 'Nakhi Bagwell', school: 'Thomas Johnson', att: 159, yds: 892, avg: 5.61, td: 5 },
          { player: 'Shemiah Hill', school: 'Oakdale', att: 104, yds: 820, avg: 7.88, td: 8 },
          { player: 'Owen Brooks', school: 'Walkersville', att: 100, yds: 764, avg: 7.6, td: 15 },
          { player: 'Ryan McLister', school: 'Middletown', att: 66, yds: 618, avg: 9.36, td: 9 },
          { player: 'Miles Robinson', school: 'Frederick', att: 93, yds: 554, avg: 6, td: 8 },
          { player: 'Ryker Pedersen', school: 'Maryland School for the Deaf', att: 85, yds: 542, avg: 6.3, td: 10 },
        ]
      },
      {
        categoryName: 'Passing',
        headers: [
            { key: 'comp', label: 'Comp' }, 
            { key: 'att', label: 'Att' }, 
            { key: 'pct', label: 'Pct' }, 
            { key: 'yds', label: 'Yds' },
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Brittin Poffenbarger', school: 'Middletown', comp: 148, att: 206, pct: '.718', yds: '2,461', td: 29 },
          { player: 'Randy Embrey', school: 'Thomas Johnson', comp: 145, att: 265, pct: '.547', yds: '2,243', td: 22 },
          { player: 'Miles Robinson', school: 'Frederick', comp: 197, att: 282, pct: '.699', yds: '2,096', td: 16 },
          { player: 'David Doy', school: 'Linganore', comp: 117, att: 172, pct: '.680', yds: '1,996', td: 28 },
          { player: 'Alex Rodriguez', school: 'Oakdale', comp: 112, att: 205, pct: '.546', yds: '1,762', td: 19 },
          { player: 'Landon Rosenberg', school: 'Tuscarora', comp: 108, att: 209, pct: '.517', yds: '1,509', td: 12 },
          { player: 'Owen Brooks', school: 'Walkersville', comp: 74, att: 163, pct: '.454', yds: '1,192', td: 9 },
          { player: 'Josh White', school: 'Urbana', comp: 69, att: 141, pct: '.489', yds: '1,124', td: 18 },
          { player: 'Chase Cregger', school: 'Catoctin', comp: 70, att: 140, pct: '.500', yds: 717, td: 4 },
          { player: 'Brady Renn', school: 'Brunswick', comp: 40, att: 87, pct: '.459', yds: 607, td: 8 },
        ]
      },
      {
        categoryName: 'Receiving',
        headers: [
            { key: 'no', label: 'No' }, 
            { key: 'yds', label: 'Yds' }, 
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Paul Huff', school: 'Frederick', no: 75, yds: 951, td: 8 },
          { player: 'Dyvae Ambush', school: 'Thomas Johnson', no: 73, yds: '1,294', td: 11 },
          { player: 'Charles Alt', school: 'Oakdale', no: 46, yds: 763, td: 8 },
          { player: 'Philip Bailey', school: 'Frederick', no: 44, yds: 325, td: 1 },
          { player: 'Joziah Cobb', school: 'Oakdale', no: 41, yds: 713, td: 9 },
          { player: 'Ronte Faunteroy', school: 'Frederick', no: 39, yds: 539, td: 5 },
          { player: 'Nathan Borawski', school: 'Middletown', no: 38, yds: 450, td: 4 },
          { player: 'Naheme Johnson', school: 'Tuscarora', no: 37, yds: 418, td: 2 },
          { player: 'Clinton Lee', school: 'Middletown', no: 35, yds: 760, td: 9 },
          { player: 'Chase Perry', school: 'Linganore', no: 34, yds: 723, td: 10 },
        ]
      }
    ]
  },
  {
    id: 'girls_flag',
    name: 'Girls Flag Football',
    standings: [
        {
          name: 'FCPS',
          headers: ['W', 'L', 'PF', 'PA'],
          rows: [
            { team: 'Linganore', w: 13, l: 0, pf: 578, pa: 137 },
            { team: 'Urbana', w: 12, l: 1, pf: 329, pa: 76 },
            { team: 'Frederick', w: 9, l: 3, pf: 228, pa: 71 },
            { team: 'Thomas Johnson', w: 7, l: 4, pf: 201, pa: 77 },
            { team: 'Oakdale', w: 6, l: 6, pf: 124, pa: 160 },
            { team: 'Middletown', w: 4, l: 7, pf: 153, pa: 185 },
            { team: 'Walkersville', w: 4, l: 7, pf: 35, pa: 187 },
            { team: 'Brunswick', w: 3, l: 8, pf: 64, pa: 238 },
            { team: 'Tuscarora', w: 2, l: 8, pf: 26, pa: 115 },
            { team: 'Catoctin', w: 1, l: 9, pf: 51, pa: 211 },
          ]
        }
    ],
    leaders: [
        {
            categoryName: 'Rushing',
            headers: [
                { key: 'att', label: 'Att' }, 
                { key: 'yds', label: 'Yds' }, 
                { key: 'avg', label: 'Avg' }, 
                { key: 'td', label: 'TD' }
            ],
            players: [
              { player: 'Rachael Hepner', school: 'Linganore', att: 44, yds: 551, avg: 12.5, td: 3 },
              { player: 'Lexi Petrie', school: 'Linganore', att: 80, yds: 468, avg: 5.9, td: 7 },
              { player: 'Brynn Bradshaw', school: 'Tuscarora', att: 56, yds: 350, avg: 6.3, td: 1 },
              { player: "Da'Myra Wallace", school: 'Frederick', att: 47, yds: 336, avg: 7.1, td: 7 },
              { player: 'Ashlyn Lackemeyer', school: 'Oakdale', att: 53, yds: 302, avg: 5.7, td: 1 },
              { player: 'Brooke Putnam', school: 'Walkersville', att: 57, yds: 280, avg: 4.9, td: '-' },
              { player: 'Morgan Booth', school: 'Oakdale', att: 31, yds: 229, avg: 7.4, td: 0 },
              { player: 'McKenna Long', school: 'Thomas Johnson', att: 36, yds: 222, avg: 6.2, td: 2 },
              { player: 'Kate Virgilio', school: 'Brunswick', att: 44, yds: 183, avg: 4.2, td: 2 },
              { player: 'Addison Shackleford', school: 'Brunswick', att: 74, yds: 159, avg: 2.1, td: 0 },
            ]
        },
        {
            categoryName: 'Passing',
            headers: [
                { key: 'comp', label: 'Comp' }, 
                { key: 'att', label: 'Att' }, 
                { key: 'pct', label: 'Pct' }, 
                { key: 'yds', label: 'Yds' },
                { key: 'td', label: 'TD' }
            ],
            players: [
              { player: 'Lexi Petrie', school: 'Linganore', comp: 320, att: 503, pct: '.636', yds: '4,180', td: 55 },
              { player: "Da'Myra Wallace", school: 'Frederick', comp: 204, att: 359, pct: '.568', yds: '2,648', td: 24 },
              { player: 'Audrey Newton', school: 'Urbana', comp: 231, att: 336, pct: '.688', yds: '2,368', td: 33 },
              { player: 'Ashlyn Lackemeyer', school: 'Oakdale', comp: 185, att: 339, pct: '.546', yds: '2,015', td: 17 },
              { player: 'Lily Trexler', school: 'Middletown', comp: 148, att: 270, pct: '.548', yds: '1,240', td: 15 },
              { player: 'McKenna Long', school: 'Thomas Johnson', comp: 95, att: 168, pct: '.565', yds: '1,067', td: 14 },
              { player: 'Addison Shackleford', school: 'Brunswick', comp: 71, att: 187, pct: '.380', yds: 638, td: 3 },
              { player: 'Brynn Bradshaw', school: 'Tuscarora', comp: 58, att: 105, pct: '.552', yds: 379, td: 2 },
            ]
        },
        {
            categoryName: 'Receiving',
            headers: [
                { key: 'no', label: 'No' }, 
                { key: 'yds', label: 'Yds' }, 
                { key: 'td', label: 'TD' }
            ],
            players: [
              { player: 'Makenna Roberts', school: 'Linganore', no: 110, yds: '1,754', td: 15 },
              { player: 'Maya Robinson', school: 'Frederick', no: 91, yds: '1,081', td: 14 },
              { player: 'Rachael Hepner', school: 'Linganore', no: 75, yds: 918, td: 22 },
              { player: 'Avery Ray', school: 'Oakdale', no: 68, yds: 801, td: 11 },
              { player: 'Avery Schneider', school: 'Middletown', no: 53, yds: 479, td: 2 },
              { player: 'Julia Duerr', school: 'Urbana', no: 49, yds: 489, td: 5 },
              { player: 'Becca Burgess', school: 'Middletown', no: 46, yds: 619, td: 5 },
              { player: 'Mackenna Patterson', school: 'Urbana', no: 44, yds: 402, td: 2 },
              { player: "Sha'Niyah Goines", school: 'Frederick', no: 43, yds: 673, td: 3 },
              { player: 'Paige Klink', school: 'Middletown', no: 42, yds: 413, td: 2 },
            ]
        }
    ]
  },
  {
    id: 'boys_soccer',
    name: 'Boys Soccer',
    standings: [
        {
            name: 'Spires Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Urbana', w: 3, l: 0, t: 0 },
                { team: 'Thomas Johnson', w: 2, l: 1, t: 0 },
                { team: 'South Hagerstown', w: 1, l: 2, t: 0 },
                { team: 'Frederick', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Potomac Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'North Hagerstown', w: 3, l: 0, t: 0 },
                { team: 'Tuscarora', w: 2, l: 1, t: 0 },
                { team: 'Oakdale', w: 1, l: 2, t: 0 },
                { team: 'Linganore', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Gambrill Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Williamsport', w: 3, l: 0, t: 0 },
                { team: 'Middletown', w: 2, l: 1, t: 0 },
                { team: 'Brunswick', w: 1, l: 2, t: 0 },
                { team: 'Walkersville', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Antietam Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Clear Spring', w: 3, l: 0, t: 0 },
                { team: 'Boonsboro', w: 2, l: 1, t: 0 },
                { team: 'Smithsburg', w: 1, l: 2, t: 0 },
                { team: 'Catoctin', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Other Schools',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: "St. John's Catholic Prep", w: 0, l: 7, t: 2 },
            ]
        }
    ],
    leaders: [
        {
            categoryName: 'Scoring Leaders',
            headers: [
                { key: 'gp', label: 'GP' }, 
                { key: 'g', label: 'G' }, 
                { key: 'a', label: 'A' }, 
                { key: 'pts', label: 'Pts' }
            ],
            players: [
                { player: 'Chris Vasquez Molina', school: 'Brunswick', gp: 15, g: 40, a: 5, pts: 85 },
                { player: "N'Tony Kalala", school: 'Tuscarora', gp: 18, g: 23, a: 11, pts: 57 },
                { player: 'Gabe Cabeza', school: 'Brunswick', gp: 18, g: 16, a: 10, pts: 42 },
                { player: 'Gabe Paschalides', school: 'Brunswick', gp: 18, g: 5, a: 24, pts: 34 },
                { player: 'Trey Glass', school: 'Catoctin', gp: 12, g: 12, a: 2, pts: 26 },
                { player: 'Wyatt Valenzuela', school: 'Linganore', gp: 13, g: 11, a: 3, pts: 25 },
                { player: 'Bryce Kenst', school: 'Urbana', gp: 17, g: 10, a: 5, pts: 25 },
                { player: 'Wilbur Ricketts', school: 'Urbana', gp: 17, g: 9, a: 7, pts: 25 },
                { player: 'Cesar Aguilar', school: 'Middletown', gp: 13, g: 10, a: 4, pts: 24 },
                { player: 'Connor Grimm', school: 'Middletown', gp: 13, g: 8, a: 6, pts: 22 },
            ]
        },
        {
            categoryName: 'Goalkeeper Statistics',
            headers: [
                { key: 'ga', label: 'GA' }, 
                { key: 'so', label: 'SO' }, 
                { key: 'sv', label: 'Sv%' }, 
                { key: 'gaa', label: 'GAA' }
            ],
            players: [
                { player: 'Ben McCarron', school: 'Urbana', ga: 5, so: 4.5, sv: '.894', gaa: 0.59 },
                { player: 'TJ Spangler', school: 'Urbana', ga: 6, so: 2.5, sv: '.870', gaa: 0.71 },
                { player: 'Andrew Barth', school: 'Oakdale', ga: 8, so: 0, sv: '.790', gaa: 0.80 },
                { player: 'Brooks Acton', school: 'Linganore', ga: 5, so: '-', sv: '-', gaa: 0.85 },
                { player: 'Aleksander Andresen', school: 'Tuscarora', ga: 17, so: '-', sv: '-', gaa: 0.94 },
                { player: 'Owen Pamplin', school: 'Oakdale', ga: 13, so: 1, sv: '.800', gaa: 1.00 },
                { player: 'Kollin Purgason', school: 'Walkersville', ga: 17, so: 6, sv: '.870', gaa: 1.06 },
                { player: 'Jack Barnes', school: 'Thomas Johnson', ga: 15, so: 3, sv: '.600', gaa: 1.25 },
            ]
        }
    ]
  },
  {
    id: 'girls_soccer',
    name: 'Girls Soccer',
    standings: [
        {
            name: 'Spires Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Urbana', w: 3, l: 0, t: 0 },
                { team: 'Frederick', w: 2, l: 1, t: 0 },
                { team: 'Thomas Johnson', w: 1, l: 2, t: 0 },
                { team: 'South Hagerstown', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Potomac Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Oakdale', w: 3, l: 0, t: 0 },
                { team: 'Linganore', w: 2, l: 1, t: 0 },
                { team: 'Tuscarora', w: 1, l: 2, t: 0 },
                { team: 'North Hagerstown', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Gambrill Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Brunswick', w: 2, l: 1, t: 0 },
                { team: 'Middletown', w: 2, l: 1, t: 0 },
                { team: 'Walkersville', w: 2, l: 1, t: 0 },
                { team: 'Williamsport', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Antietam Division',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: 'Smithsburg', w: 3, l: 0, t: 0 },
                { team: 'Boonsboro', w: 2, l: 1, t: 0 },
                { team: 'Catoctin', w: 1, l: 2, t: 0 },
                { team: 'Clear Spring', w: 0, l: 3, t: 0 },
            ]
        },
        {
            name: 'Other Schools',
            headers: ['W', 'L', 'T'],
            rows: [
                { team: "St. John's Catholic Prep", w: 2, l: 10, t: 0 },
            ]
        }
    ],
    leaders: [
        {
            categoryName: 'Scoring Leaders',
            headers: [
                { key: 'gp', label: 'GP' }, 
                { key: 'g', label: 'G' }, 
                { key: 'a', label: 'A' }, 
                { key: 'pts', label: 'Pts' }
            ],
            players: [
                { player: 'Brooke Clagett', school: 'Oakdale', gp: 17, g: 27, a: 4, pts: 58 },
                { player: 'Emily Feaster', school: 'Oakdale', gp: 19, g: 14, a: 3, pts: 31 },
                { player: 'Adalyn DeGrange', school: 'Catoctin', gp: 13, g: 8, a: 10, pts: 26 },
                { player: 'Olivia Baker', school: 'Catoctin', gp: 13, g: 10, a: 5, pts: 25 },
                { player: 'Fiona Collins', school: 'Oakdale', gp: 19, g: 7, a: 10, pts: 24 },
                { player: 'Laila Jackson', school: 'Brunswick', gp: 16, g: 9, a: 4, pts: 22 },
                { player: 'Jamisyn Kenyatta', school: 'Frederick', gp: 13, g: 10, a: 2, pts: 22 },
                { player: 'Emilee Schwier', school: 'Linganore', gp: 16, g: 9, a: 4, pts: 22 },
                { player: 'Katie Hargett', school: 'Brunswick', gp: 16, g: 5, a: 10, pts: 20 },
                { player: 'Mackenzie Thompson', school: 'Linganore', gp: 16, g: 8, a: 4, pts: 20 },
            ]
        },
        {
            categoryName: 'Goalkeeper Statistics',
            headers: [
                { key: 'ga', label: 'GA' }, 
                { key: 'so', label: 'SO' }, 
                { key: 'sv', label: 'Sv%' }, 
                { key: 'gaa', label: 'GAA' }
            ],
            players: [
                { player: 'Makayla Olenchalk', school: 'Middletown', ga: 2, so: 0, sv: '.909', gaa: 0.41 },
                { player: 'Brynn Clagett', school: 'Oakdale', ga: 8, so: 15, sv: '-', gaa: 0.44 },
                { player: 'Emily Krichbaum', school: 'Middletown', ga: 5, so: 2, sv: '.915', gaa: 0.52 },
                { player: 'Hannah Cook', school: 'Brunswick', ga: 6, so: 3, sv: '.895', gaa: 0.78 },
                { player: 'Paige Miller', school: 'Walkersville', ga: 12, so: 8, sv: '-', gaa: 0.85 },
                { player: 'Hannah Zirk', school: 'Linganore', ga: 13, so: 6, sv: '.847', gaa: 1.0 },
                { player: 'Chandler Ways', school: 'Urbana', ga: '-', so: 3.5, sv: '-', gaa: 1.19 },
            ]
        }
    ]
  },
  {
    id: 'volleyball',
    name: 'Volleyball',
    standings: [
        {
            name: 'Spires Division',
            headers: ['W', 'L'],
            rows: [
                { team: 'Urbana', w: 3, l: 0 },
                { team: 'Frederick', w: 2, l: 1 },
                { team: 'Thomas Johnson', w: 1, l: 2 },
                { team: 'South Hagerstown', w: 0, l: 3 },
            ]
        },
        {
            name: 'Potomac Division',
            headers: ['W', 'L'],
            rows: [
                { team: 'Linganore', w: 3, l: 0 },
                { team: 'Tuscarora', w: 2, l: 1 },
                { team: 'North Hagerstown', w: 1, l: 2 },
                { team: 'Oakdale', w: 0, l: 3 },
            ]
        },
        {
            name: 'Gambrill Division',
            headers: ['W', 'L'],
            rows: [
                { team: 'Williamsport', w: 2, l: 1 },
                { team: 'Brunswick', w: 2, l: 1 },
                { team: 'Walkersville', w: 2, l: 1 },
                { team: 'Middletown', w: 0, l: 3 },
            ]
        },
        {
            name: 'Antietam Division',
            headers: ['W', 'L'],
            rows: [
                { team: 'Clear Spring', w: 3, l: 0 },
                { team: 'Catoctin', w: 1, l: 2 },
                { team: 'Smithsburg', w: 1, l: 2 },
                { team: 'Boonsboro', w: 1, l: 2 },
            ]
        },
        {
            name: 'Other Schools',
            headers: ['W', 'L'],
            rows: [
                { team: 'Maryland School for the Deaf', w: 18, l: 2 },
                { team: "St. John's Catholic Prep", w: 5, l: 10 },
            ]
        }
    ],
    leaders: [
        {
            categoryName: 'Kills',
            headers: [
                { key: 'sp', label: 'SP' }, 
                { key: 'kills', label: 'Kills' }, 
                { key: 'hit', label: 'Hit%' }, 
                { key: 'avg', label: 'Avg' }
            ],
            players: [
                { player: 'Maliyah Coleman', school: 'Maryland School for the Deaf', sp: 99, kills: 534, hit: '.314', avg: 5.39 },
                { player: 'Nikita Dzougoutov', school: 'Maryland School for the Deaf', sp: 91, kills: 349, hit: '.236', avg: 3.84 },
                { player: 'Jocelyn Miller', school: 'Middletown', sp: 55, kills: 189, hit: '.256', avg: 3.44 },
                { player: 'Kaniyah Ball', school: 'Frederick', sp: 45, kills: 153, hit: '.149', avg: 3.40 },
                { player: 'Lily King', school: 'Tuscarora', sp: 55, kills: 161, hit: '.202', avg: 2.93 },
                { player: 'Ella Grove', school: "St. John's Catholic Prep", sp: 72, kills: 210, hit: '.130', avg: 2.92 },
                { player: 'Raylin Horst', school: 'Thomas Johnson', sp: 62, kills: 171, hit: '-', avg: 2.76 },
                { player: 'Ivory Boone', school: 'Urbana', sp: 34, kills: 92, hit: '.423', avg: 2.71 },
                { player: 'Simone Assasie', school: 'Urbana', sp: 34, kills: 87, hit: '.300', avg: 2.56 },
                { player: 'Amy Latimer', school: 'Linganore', sp: 58, kills: 147, hit: '-', avg: 2.53 },
            ]
        },
        {
            categoryName: 'Assists',
            headers: [
                { key: 'asts', label: 'Asts' }, 
                { key: 'digs', label: 'Digs' }, 
                { key: 'avg', label: 'Avg' }
            ],
            players: [
                { player: 'Emma Le', school: 'Maryland School for the Deaf', asts: 100, digs: 879, avg: 8.79 },
                { player: 'Charlye Wood', school: 'Middletown', asts: 59, digs: 440, avg: 7.46 },
                { player: 'Adelle Kusi', school: 'Oakdale', asts: 61, digs: 426, avg: 6.98 },
                { player: 'Kendall Ortiz', school: 'Frederick', asts: 45, digs: 314, avg: 6.98 },
                { player: 'Charis Burge', school: 'Urbana', asts: 36, digs: 193, avg: 5.36 },
                { player: 'Lili\'uokalani Primacio', school: "St. John's Catholic Prep", asts: 73, digs: 390, avg: 5.34 },
                { player: 'Zayna Brooks', school: 'Tuscarora', asts: 55, digs: 266, avg: 4.84 },
                { player: 'Julia Tomaski', school: 'Linganore', asts: 58, digs: 242, avg: 4.17 },
                { player: 'Saya Chin', school: 'Thomas Johnson', asts: 62, digs: 251, avg: 4.05 },
                { player: 'Serena Treadwell', school: 'Tuscarora', asts: 55, digs: 213, avg: 3.87 },
            ]
        },
        {
            categoryName: 'Digs',
            headers: [
                { key: 'sp', label: 'SP' }, 
                { key: 'digs', label: 'Digs' }, 
                { key: 'avg', label: 'Avg' }
            ],
            players: [
                { player: 'Kaniyah Ball', school: 'Frederick', sp: 45, digs: 232, avg: 5.16 },
                { player: 'Makenzie Shearer', school: 'Linganore', sp: 58, digs: 244, avg: 4.21 },
                { player: 'Lilah Colbert', school: 'Oakdale', sp: 60, digs: 250, avg: 4.17 },
                { player: 'Bella Brown', school: 'Thomas Johnson', sp: 49, digs: 204, avg: 4.16 },
                { player: 'Talia DoCarmo', school: 'Urbana', sp: 35, digs: 130, avg: 3.71 },
                { player: 'Megan Jay', school: 'Tuscarora', sp: 55, digs: 201, avg: 3.65 },
                { player: 'Kailyn Bryant', school: 'Frederick', sp: 45, digs: 157, avg: 3.49 },
                { player: 'Raylin Horst', school: 'Thomas Johnson', sp: 62, digs: 194, avg: 3.13 },
                { player: 'Lily King', school: 'Tuscarora', sp: 55, digs: 168, avg: 3.05 },
                { player: 'Zayna Brooks', school: 'Tuscarora', sp: 55, digs: 148, avg: 2.69 },
            ]
        }
    ]
  },
  {
      id: 'field_hockey',
      name: 'Field Hockey',
      standings: [
          {
              name: 'Large School',
              headers: ['W', 'L', 'T'],
              rows: [
                  { team: 'Linganore', w: 5, l: 0, t: 0 },
                  { team: 'Urbana', w: 4, l: 1, t: 0 },
                  { team: 'Oakdale', w: 3, l: 2, t: 0 },
                  { team: 'Frederick', w: 2, l: 3, t: 0 },
                  { team: 'Tuscarora', w: 1, l: 4, t: 0 },
                  { team: 'Thomas Johnson', w: 0, l: 5, t: 0 },
              ]
          },
          {
              name: 'Small School',
              headers: ['W', 'L', 'T'],
              rows: [
                  { team: 'Walkersville', w: 3, l: 0, t: 0 },
                  { team: 'Catoctin', w: 2, l: 1, t: 0 },
                  { team: 'Middletown', w: 1, l: 2, t: 0 },
                  { team: 'Brunswick', w: 0, l: 3, t: 0 },
              ]
          }
      ],
      leaders: [
          {
              categoryName: 'Scoring Leaders',
              headers: [
                  { key: 'gp', label: 'GP' }, 
                  { key: 'g', label: 'G' }, 
                  { key: 'a', label: 'A' }, 
                  { key: 'pts', label: 'Pts' }
              ],
              players: [
                  { player: 'Lexi Bristow', school: 'Urbana', gp: 17, g: 19, a: 15, pts: 53 },
                  { player: 'Mia Marquart', school: 'Walkersville', gp: 15, g: 20, a: 12, pts: 52 },
                  { player: 'Makenzie Kilcoyne', school: 'Urbana', gp: 17, g: 19, a: 14, pts: 52 },
                  { player: 'Reese Rymon', school: 'Oakdale', gp: 16, g: 21, a: 8, pts: 50 },
                  { player: 'Josey Shaffer', school: 'Catoctin', gp: 15, g: 18, a: 9, pts: 45 },
                  { player: 'Maddie Myers', school: 'Catoctin', gp: 15, g: 21, a: 1, pts: 43 },
                  { player: 'Autumn Jordan', school: 'Linganore', gp: 20, g: 16, a: 9, pts: 41 },
                  { player: 'Addison Ridgely', school: 'Linganore', gp: 20, g: 16, a: 7, pts: 39 },
                  { player: 'Brianna McGuirl', school: 'Linganore', gp: 20, g: 17, a: 2, pts: 36 },
                  { player: 'Amaya Perera', school: 'Urbana', gp: 17, g: 12, a: 11, pts: 35 },
              ]
          },
          {
              categoryName: 'Goalkeeper Statistics',
              headers: [
                  { key: 'gp', label: 'GP' }, 
                  { key: 'ga', label: 'GA' }, 
                  { key: 'so', label: 'SO' }, 
                  { key: 'sv', label: 'Sv%' }, 
                  { key: 'gaa', label: 'GAA' }
              ],
              players: [
                  { player: 'Katie Schmitt', school: 'Urbana', gp: 14.25, ga: 11, so: 7.5, sv: '.770', gaa: 0.45 },
                  { player: 'Allena Jaworski', school: 'Linganore', gp: 20, ga: 17, so: 10, sv: '.910', gaa: 0.89 },
                  { player: 'Liya Yemane', school: 'Oakdale', gp: 6.5, ga: 7, so: 4.5, sv: '.770', gaa: 1.08 },
                  { player: 'Iris Mokashi', school: 'Oakdale', gp: 7.5, ga: 11, so: 3, sv: '.830', gaa: 1.47 },
                  { player: 'Alexi Jones', school: 'Walkersville', gp: 14, ga: 25, so: 7, sv: '.725', gaa: 1.96 },
                  { player: 'Charlotte Felton', school: 'Middletown', gp: 15, ga: 33, so: 6, sv: '.708', gaa: 2.15 },
                  { player: 'Vivian Lewis', school: 'Catoctin', gp: 15, ga: 38, so: 2, sv: '.768', gaa: 2.53 },
              ]
          }
      ]
  },
  {
      id: 'cross_country',
      name: 'Cross Country',
      standings: [],
      leaders: [
          {
              categoryName: 'Top 5K Times - Boys',
              headers: [{ key: 'time', label: 'Time' }],
              players: [
                  { player: 'Joshua Rothery', school: 'Urbana', time: '15:50.6' },
                  { player: 'Patrick Salter', school: 'Oakdale', time: '15:52.4' },
                  { player: 'Riley Gallogly', school: 'Urbana', time: '15:56.5' },
                  { player: 'Korey Kauflin', school: 'Urbana', time: '15:57.9' },
                  { player: 'Asher Adelman', school: 'Brunswick', time: '16:03.2' },
                  { player: 'Evan Madraymootoo', school: 'Urbana', time: '16:03.7' },
                  { player: 'Simon McGillivray', school: 'Brunswick', time: '16:04.3' },
                  { player: 'Cole Cline', school: 'Urbana', time: '16:04.4' },
                  { player: 'Miles Ghim', school: 'Thomas Johnson', time: '16:10.4' },
                  { player: 'Dashiell Wexler', school: 'Thomas Johnson', time: '16:10.5' },
              ]
          },
          {
              categoryName: 'Top 5K Times - Girls',
              headers: [{ key: 'time', label: 'Time' }],
              players: [
                  { player: 'Kate Miner', school: 'Urbana', time: '18:35.2' },
                  { player: 'Hailey Lane', school: 'Tuscarora', time: '18:39.6' },
                  { player: 'MadeleneKate Partlow', school: 'Thomas Johnson', time: '18:58.9' },
                  { player: 'Natalie Barber', school: 'Urbana', time: '19:03.1' },
                  { player: 'Samantha Whiteman', school: 'Linganore', time: '19:06.6' },
                  { player: 'Siena Foster', school: 'Tuscarora', time: '19:16.8' },
                  { player: 'Maya Osher', school: 'Urbana', time: '19:22.2' },
                  { player: 'Leticia Detrow', school: 'Maryland School for the Deaf', time: '19:26.2' },
                  { player: 'Yasmeena Hassen Friess', school: 'Frederick', time: '19:37.5' },
                  { player: 'Rachel Herbst', school: 'Thomas Johnson', time: '19:58.4' },
              ]
          }
      ]
  },
  {
      id: 'golf',
      name: 'Golf',
      standings: [],
      leaders: [
          {
              categoryName: '9-Hole Average',
              headers: [{ key: 'avg', label: 'Avg' }],
              players: [
                  { player: 'Landon Tudor', school: 'Oakdale', avg: 35.0 },
                  { player: 'Callen Edmonston', school: 'Catoctin', avg: 36.4 },
                  { player: 'Cooper Moskowitz', school: 'Middletown', avg: 37.4 },
                  { player: 'Claire Son', school: 'Urbana', avg: 38.0 },
                  { player: 'Zac Taylor', school: 'Oakdale', avg: 38.4 },
                  { player: 'Clayton Bowman', school: 'Urbana', avg: 38.6 },
                  { player: 'Caden Roosa', school: 'Oakdale', avg: 38.8 },
                  { player: 'Ollie Witt', school: 'Middletown', avg: 39.0 },
                  { player: 'Celine Lieu', school: 'Walkersville', avg: 39.2 },
                  { player: 'Aidan Nilan', school: 'Oakdale', avg: 39.2 },
              ]
          }
      ]
  }
];