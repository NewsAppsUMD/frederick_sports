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
          { player: 'Ty Ross', school: 'Brunswick', att: 98, yds: 498, avg: 5.1, td: 4 },
          { player: 'Grant Smith', school: 'Middletown', att: 75, yds: 485, avg: 6.4, td: 6 },
          { player: 'Jayden Washington', school: 'Tuscarora', att: 110, yds: 450, avg: 4.1, td: 3 },
          { player: 'Luke Miller', school: 'Urbana', att: 82, yds: 420, avg: 5.1, td: 5 },
          { player: 'Chase Williams', school: 'Linganore', att: 55, yds: 380, avg: 6.9, td: 4 },
          { player: 'Devin Thomas', school: 'Catoctin', att: 88, yds: 375, avg: 4.2, td: 3 },
          { player: 'Marcus Lee', school: 'Thomas Johnson', att: 60, yds: 350, avg: 5.8, td: 2 },
          { player: 'Jordan Wright', school: 'Urbana', att: 55, yds: 320, avg: 5.8, td: 4 },
          { player: 'Cameron Hall', school: 'Tuscarora', att: 70, yds: 310, avg: 4.4, td: 2 },
          { player: 'Xavier Brown', school: 'Frederick', att: 45, yds: 290, avg: 6.4, td: 3 }
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
          { player: 'Landon Rosenberg', school: 'Tuscarora', comp: 108, att: 209, pct: '.517', yds: '1,280', td: 10 },
          { player: 'Ethan Long', school: 'Brunswick', comp: 95, att: 180, pct: '.527', yds: '1,150', td: 8 },
          { player: 'Caleb Jones', school: 'Walkersville', comp: 88, att: 165, pct: '.533', yds: '1,050', td: 11 },
          { player: 'Trey Taylor', school: 'Urbana', comp: 72, att: 140, pct: '.514', yds: '980', td: 7 },
          { player: 'Evan Wilson', school: 'Catoctin', comp: 65, att: 130, pct: '.500', yds: '850', td: 5 },
          { player: 'Connor Murphy', school: 'Middletown', comp: 50, att: 90, pct: '.555', yds: '720', td: 6 },
          { player: 'Logan White', school: 'Oakdale', comp: 45, att: 85, pct: '.529', yds: '650', td: 4 },
          { player: 'Gavin Green', school: 'Linganore', comp: 30, att: 50, pct: '.600', yds: '450', td: 5 },
          { player: 'Tyler Scott', school: 'Walkersville', comp: 35, att: 70, pct: '.500', yds: '410', td: 2 },
          { player: 'Blake Hill', school: 'Maryland School for the Deaf', comp: 25, att: 55, pct: '.454', yds: '380', td: 3 }
        ]
      },
      {
        categoryName: 'Receiving',
        headers: [
            { key: 'rec', label: 'Rec' }, 
            { key: 'yds', label: 'Yds' }, 
            { key: 'avg', label: 'Avg' }, 
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Hunter Thompson', school: 'Oakdale', rec: 52, yds: '985', avg: 18.9, td: 12 },
          { player: 'Jameson Smith', school: 'Linganore', rec: 48, yds: '870', avg: 18.1, td: 14 },
          { player: 'Ryan Miller', school: 'Middletown', rec: 45, yds: '750', avg: 16.6, td: 9 },
          { player: 'Kaden Johnson', school: 'Thomas Johnson', rec: 42, yds: '680', avg: 16.2, td: 7 },
          { player: 'Liam O\'Connor', school: 'Urbana', rec: 38, yds: '590', avg: 15.5, td: 5 },
          { player: 'Tyler Brown', school: 'Frederick', rec: 35, yds: '540', avg: 15.4, td: 4 },
          { player: 'Mason Davis', school: 'Walkersville', rec: 32, yds: '480', avg: 15.0, td: 6 },
          { player: 'Carter Wilson', school: 'Tuscarora', rec: 30, yds: '450', avg: 15.0, td: 3 },
          { player: 'Noah Garcia', school: 'Brunswick', rec: 28, yds: '410', avg: 14.6, td: 2 },
          { player: 'Elijah Thomas', school: 'Catoctin', rec: 25, yds: '350', avg: 14.0, td: 1 },
          { player: 'Dylan Young', school: 'Linganore', rec: 22, yds: '330', avg: 15.0, td: 2 },
          { player: 'Austin King', school: 'Middletown', rec: 20, yds: '310', avg: 15.5, td: 3 },
          { player: 'Brandon Clark', school: 'Urbana', rec: 18, yds: '290', avg: 16.1, td: 1 },
          { player: 'Kevin Lewis', school: 'Frederick', rec: 15, yds: '250', avg: 16.6, td: 2 },
          { player: 'Justin Adams', school: 'Oakdale', rec: 14, yds: '220', avg: 15.7, td: 1 }
        ]
      },
      {
        categoryName: 'Tackles',
        headers: [
            { key: 'tot', label: 'Total' },
            { key: 'solo', label: 'Solo' },
            { key: 'asst', label: 'Asst' },
            { key: 'sacks', label: 'Sacks' }
        ],
        players: [
          { player: 'Zachary White', school: 'Linganore', tot: 115, solo: 75, asst: 40, sacks: 8.5 },
          { player: 'Brendan Kelly', school: 'Urbana', tot: 105, solo: 60, asst: 45, sacks: 6.0 },
          { player: 'Justin Reed', school: 'Oakdale', tot: 98, solo: 58, asst: 40, sacks: 7.0 },
          { player: 'Connor Murphy', school: 'Middletown', tot: 92, solo: 55, asst: 37, sacks: 5.5 },
          { player: 'Dylan Carter', school: 'Walkersville', tot: 88, solo: 50, asst: 38, sacks: 4.0 },
          { player: 'Jordan Evans', school: 'Thomas Johnson', tot: 85, solo: 48, asst: 37, sacks: 3.5 },
          { player: 'Caleb King', school: 'Frederick', tot: 82, solo: 45, asst: 37, sacks: 2.0 },
          { player: 'Nathan Scott', school: 'Tuscarora', tot: 78, solo: 42, asst: 36, sacks: 3.0 },
          { player: 'Aaron Lewis', school: 'Brunswick', tot: 75, solo: 40, asst: 35, sacks: 2.5 },
          { player: 'Isaac Clark', school: 'Catoctin', tot: 70, solo: 38, asst: 32, sacks: 1.5 },
          { player: 'Ryan Cooper', school: 'Linganore', tot: 65, solo: 35, asst: 30, sacks: 1.0 },
          { player: 'Eric Turner', school: 'Middletown', tot: 62, solo: 32, asst: 30, sacks: 2.5 },
          { player: 'Mike Johnson', school: 'Walkersville', tot: 60, solo: 30, asst: 30, sacks: 1.5 },
          { player: 'Chris Baker', school: 'Urbana', tot: 58, solo: 28, asst: 30, sacks: 0.5 },
          { player: 'David Martinez', school: 'Tuscarora', tot: 55, solo: 25, asst: 30, sacks: 1.0 }
        ]
      }
    ]
  },
  {
    id: 'girls-flag-football',
    name: 'Girls Flag Football',
    standings: [
      {
        name: 'FCPS',
        headers: ['W', 'L', 'PF', 'PA'],
        rows: [
          { team: 'Linganore', w: 13, l: 3, pf: 400, pa: 127 },
          { team: 'Urbana', w: 12, l: 1, pf: 380, pa: 100 },
          { team: 'Frederick', w: 9, l: 4, pf: 250, pa: 180 },
          { team: 'Thomas Johnson', w: 7, l: 6, pf: 200, pa: 210 },
          { team: 'Middletown', w: 6, l: 7, pf: 180, pa: 200 },
          { team: 'Oakdale', w: 5, l: 8, pf: 150, pa: 250 },
          { team: 'Walkersville', w: 4, l: 9, pf: 120, pa: 280 },
          { team: 'Tuscarora', w: 2, l: 11, pf: 90, pa: 320 },
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Passing',
        headers: [
            { key: 'comp', label: 'Comp' },
            { key: 'yds', label: 'Yds' },
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Sarah Jenkins', school: 'Urbana', comp: 145, yds: '2,100', td: 35 },
          { player: 'Emily Clark', school: 'Linganore', comp: 130, yds: '1,950', td: 30 },
          { player: 'Jessica Davis', school: 'Frederick', comp: 115, yds: '1,600', td: 22 },
          { player: 'Ashley Brown', school: 'Thomas Johnson', comp: 100, yds: '1,400', td: 18 },
          { player: 'Megan Wilson', school: 'Middletown', comp: 95, yds: '1,300', td: 15 },
          { player: 'Rachel Moore', school: 'Oakdale', comp: 90, yds: '1,200', td: 12 },
          { player: 'Samantha Taylor', school: 'Walkersville', comp: 80, yds: '1,000', td: 10 },
          { player: 'Olivia Anderson', school: 'Tuscarora', comp: 60, yds: '800', td: 5 },
          { player: 'Chloe Evans', school: 'Brunswick', comp: 55, yds: '750', td: 8 },
          { player: 'Natalie Hall', school: 'Catoctin', comp: 50, yds: '700', td: 6 },
          { player: 'Grace Turner', school: 'Urbana', comp: 45, yds: '650', td: 5 },
          { player: 'Mia Scott', school: 'Linganore', comp: 40, yds: '600', td: 4 },
          { player: 'Ava Roberts', school: 'Middletown', comp: 35, yds: '550', td: 3 }
        ]
      },
      {
        categoryName: 'Rushing',
        headers: [
            { key: 'att', label: 'Att' },
            { key: 'yds', label: 'Yds' },
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Chloe Thompson', school: 'Linganore', att: 90, yds: '950', td: 18 },
          { player: 'Madison Martinez', school: 'Urbana', att: 85, yds: '850', td: 15 },
          { player: 'Hannah Robinson', school: 'Frederick', att: 80, yds: '750', td: 12 },
          { player: 'Kayla White', school: 'Thomas Johnson', att: 75, yds: '650', td: 10 },
          { player: 'Lauren Harris', school: 'Middletown', att: 70, yds: '600', td: 8 },
          { player: 'Sydney Clark', school: 'Oakdale', att: 65, yds: '550', td: 6 },
          { player: 'Morgan Lewis', school: 'Walkersville', att: 60, yds: '500', td: 5 },
          { player: 'Taylor Walker', school: 'Tuscarora', att: 50, yds: '400', td: 3 },
          { player: 'Sophia King', school: 'Brunswick', att: 45, yds: '380', td: 4 },
          { player: 'Isabella Wright', school: 'Catoctin', att: 40, yds: '350', td: 3 },
          { player: 'Emma Green', school: 'Urbana', att: 35, yds: '320', td: 2 },
          { player: 'Charlotte Hill', school: 'Linganore', att: 30, yds: '300', td: 2 },
          { player: 'Amelia Baker', school: 'Middletown', att: 25, yds: '280', td: 1 }
        ]
      }
    ]
  },
  {
    id: 'boys-soccer',
    name: 'Boys Soccer',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L', 'T'],
        rows: [
          { team: 'Tuscarora', w: 14, l: 2, t: 1 },
          { team: 'Urbana', w: 13, l: 3, t: 1 },
          { team: 'Linganore', w: 11, l: 4, t: 2 },
          { team: 'Brunswick', w: 10, l: 5, t: 3 },
          { team: 'Middletown', w: 9, l: 6, t: 1 },
          { team: 'Oakdale', w: 8, l: 7, t: 2 },
          { team: 'Frederick', w: 6, l: 9, t: 1 },
          { team: 'Thomas Johnson', w: 5, l: 10, t: 0 },
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Goals',
        headers: [{ key: 'g', label: 'Goals' }],
        players: [
          { player: 'Carlos Mendez', school: 'Tuscarora', g: 22 },
          { player: 'Liam Anderson', school: 'Urbana', g: 19 },
          { player: 'Ethan Turner', school: 'Brunswick', g: 17 },
          { player: 'Noah Roberts', school: 'Linganore', g: 15 },
          { player: 'Aiden Campbell', school: 'Oakdale', g: 14 },
          { player: 'Lucas Scott', school: 'Middletown', g: 12 },
          { player: 'Mason Green', school: 'Frederick', g: 10 },
          { player: 'Julian King', school: 'Thomas Johnson', g: 9 },
          { player: 'Elijah Baker', school: 'Tuscarora', g: 8 },
          { player: 'Caleb Evans', school: 'Urbana', g: 7 },
          { player: 'Ryan Adams', school: 'Brunswick', g: 6 },
          { player: 'Tyler Wilson', school: 'Walkersville', g: 6 },
          { player: 'Justin Lee', school: 'Oakdale', g: 5 },
          { player: 'Brandon Hall', school: 'Middletown', g: 5 },
          { player: 'Kevin White', school: 'Linganore', g: 4 }
        ]
      },
      {
        categoryName: 'Assists',
        headers: [{ key: 'a', label: 'Assists' }],
        players: [
          { player: 'Noah Roberts', school: 'Linganore', a: 15 },
          { player: 'Carlos Mendez', school: 'Tuscarora', a: 12 },
          { player: 'Liam Anderson', school: 'Urbana', a: 10 },
          { player: 'Ethan Turner', school: 'Brunswick', a: 9 },
          { player: 'Lucas Scott', school: 'Middletown', a: 8 },
          { player: 'Aiden Campbell', school: 'Oakdale', a: 7 },
          { player: 'Mason Green', school: 'Frederick', a: 6 },
          { player: 'Julian King', school: 'Thomas Johnson', a: 5 },
          { player: 'Elijah Baker', school: 'Tuscarora', a: 4 },
          { player: 'Caleb Evans', school: 'Urbana', a: 4 },
          { player: 'Ryan Adams', school: 'Brunswick', a: 3 },
          { player: 'Tyler Wilson', school: 'Walkersville', a: 3 },
          { player: 'Justin Lee', school: 'Oakdale', a: 3 },
          { player: 'Brandon Hall', school: 'Middletown', a: 2 },
          { player: 'Kevin White', school: 'Linganore', a: 2 }
        ]
      }
    ]
  },
  {
    id: 'girls-soccer',
    name: 'Girls Soccer',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L', 'T'],
        rows: [
          { team: 'Oakdale', w: 15, l: 1, t: 1 },
          { team: 'Linganore', w: 13, l: 3, t: 1 },
          { team: 'Brunswick', w: 12, l: 4, t: 0 },
          { team: 'Middletown', w: 10, l: 5, t: 2 },
          { team: 'Urbana', w: 9, l: 6, t: 1 },
          { team: 'Walkersville', w: 7, l: 8, t: 1 },
          { team: 'Tuscarora', w: 5, l: 10, t: 2 },
          { team: 'Frederick', w: 4, l: 11, t: 0 },
        ]
      }
    ],
    leaders: [
        {
        categoryName: 'Goals',
        headers: [{ key: 'g', label: 'Goals' }],
        players: [
          { player: 'Sophia Martinez', school: 'Oakdale', g: 20 },
          { player: 'Isabella Garcia', school: 'Linganore', g: 18 },
          { player: 'Ava Robinson', school: 'Brunswick', g: 16 },
          { player: 'Mia Clark', school: 'Middletown', g: 14 },
          { player: 'Charlotte Lewis', school: 'Urbana', g: 12 },
          { player: 'Amelia Walker', school: 'Walkersville', g: 10 },
          { player: 'Harper Hall', school: 'Tuscarora', g: 8 },
          { player: 'Evelyn Young', school: 'Frederick', g: 6 },
          { player: 'Abigail King', school: 'Oakdale', g: 5 },
          { player: 'Ella Wright', school: 'Linganore', g: 4 },
          { player: 'Lily Thompson', school: 'Middletown', g: 4 },
          { player: 'Zoe Clark', school: 'Urbana', g: 3 },
          { player: 'Madison Lewis', school: 'Walkersville', g: 3 },
          { player: 'Chloe Walker', school: 'Brunswick', g: 3 },
          { player: 'Layla Robinson', school: 'Frederick', g: 2 }
        ]
      },
      {
        categoryName: 'Assists',
        headers: [{ key: 'a', label: 'Assists' }],
        players: [
          { player: 'Isabella Garcia', school: 'Linganore', a: 12 },
          { player: 'Sophia Martinez', school: 'Oakdale', a: 10 },
          { player: 'Ava Robinson', school: 'Brunswick', a: 8 },
          { player: 'Mia Clark', school: 'Middletown', a: 7 },
          { player: 'Charlotte Lewis', school: 'Urbana', a: 6 },
          { player: 'Amelia Walker', school: 'Walkersville', a: 5 },
          { player: 'Harper Hall', school: 'Tuscarora', a: 4 },
          { player: 'Evelyn Young', school: 'Frederick', a: 3 },
          { player: 'Abigail King', school: 'Oakdale', a: 2 },
          { player: 'Ella Wright', school: 'Linganore', a: 1 },
          { player: 'Lily Thompson', school: 'Middletown', a: 1 },
          { player: 'Zoe Clark', school: 'Urbana', a: 1 },
          { player: 'Madison Lewis', school: 'Walkersville', a: 1 },
          { player: 'Chloe Walker', school: 'Brunswick', a: 1 },
          { player: 'Layla Robinson', school: 'Frederick', a: 1 }
        ]
      }
    ]
  },
  {
    id: 'volleyball',
    name: 'Volleyball',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L'],
        rows: [
          { team: 'Urbana', w: 18, l: 2 },
          { team: 'Tuscarora', w: 16, l: 4 },
          { team: 'Oakdale', w: 14, l: 5 },
          { team: 'MSD', w: 12, l: 6 },
          { team: 'Linganore', w: 10, l: 8 },
          { team: 'Middletown', w: 9, l: 9 },
          { team: 'Frederick', w: 6, l: 12 },
        ]
      }
    ],
    leaders: []
  },
  {
    id: 'field-hockey',
    name: 'Field Hockey',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L', 'T'],
        rows: [
          { team: 'Linganore', w: 14, l: 2, t: 0 },
          { team: 'Urbana', w: 13, l: 3, t: 1 },
          { team: 'Walkersville', w: 11, l: 5, t: 0 },
          { team: 'Oakdale', w: 10, l: 6, t: 1 },
          { team: 'Middletown', w: 8, l: 7, t: 2 },
          { team: 'Frederick', w: 5, l: 10, t: 0 },
        ]
      }
    ],
    leaders: []
  },
  {
    id: 'boys-cross-country',
    name: 'Boys Cross Country',
    standings: [
      {
        name: 'Championship Results',
        headers: ['Points'],
        rows: [
          { team: 'Urbana', points: 32 },
          { team: 'Thomas Johnson', points: 58 },
          { team: 'Brunswick', points: 85 },
          { team: 'Oakdale', points: 112 },
          { team: 'Linganore', points: 125 },
          { team: 'Tuscarora', points: 140 },
          { team: 'Middletown', points: 165 },
          { team: 'Frederick', points: 190 }
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Top Times (5K)',
        headers: [{ key: 'time', label: 'Time' }],
        players: [
          { player: 'David Rodenhaver', school: 'Urbana', time: '15:42' },
          { player: 'James Partlow', school: 'Thomas Johnson', time: '15:55' },
          { player: 'Caleb Tenney', school: 'Brunswick', time: '16:10' },
          { player: 'Jakob Werdell', school: 'Oakdale', time: '16:15' },
          { player: 'Seth Barron', school: 'Urbana', time: '16:22' },
          { player: 'Griffin Poffenbarger', school: 'Middletown', time: '16:30' },
          { player: 'Luke Sague', school: 'Linganore', time: '16:35' },
          { player: 'Ryan Brightman', school: 'Tuscarora', time: '16:40' },
          { player: 'Evan Quinn', school: 'Frederick', time: '16:45' },
          { player: 'Kyle Walker', school: 'Linganore', time: '16:50' },
          { player: 'Sam Oliver', school: 'Urbana', time: '16:55' },
          { player: 'Ben King', school: 'Thomas Johnson', time: '17:00' },
          { player: 'Alex Davis', school: 'Oakdale', time: '17:05' },
          { player: 'Cole Jones', school: 'Brunswick', time: '17:10' },
          { player: 'Nathan Brown', school: 'Middletown', time: '17:15' }
        ]
      }
    ]
  },
  {
    id: 'girls-cross-country',
    name: 'Girls Cross Country',
    standings: [
      {
        name: 'Championship Results',
        headers: ['Points'],
        rows: [
          { team: 'Urbana', points: 28 },
          { team: 'Thomas Johnson', points: 65 },
          { team: 'Frederick', points: 90 },
          { team: 'Tuscarora', points: 115 },
          { team: 'Oakdale', points: 130 },
          { team: 'Linganore', points: 145 },
          { team: 'Brunswick', points: 160 },
          { team: 'Middletown', points: 185 }
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Top Times (5K)',
        headers: [{ key: 'time', label: 'Time' }],
        players: [
          { player: 'Ivy Coldren', school: 'Urbana', time: '18:10' },
          { player: 'Caroline Gregory', school: 'Frederick', time: '18:25' },
          { player: 'Hailey Lane', school: 'Tuscarora', time: '18:40' },
          { player: 'Grace Humbert', school: 'Thomas Johnson', time: '18:55' },
          { player: 'Audrey Meadows', school: 'Urbana', time: '19:10' },
          { player: 'Lucy Clark', school: 'Oakdale', time: '19:20' },
          { player: 'Sarah Anderson', school: 'Linganore', time: '19:30' },
          { player: 'Maya Wilson', school: 'Thomas Johnson', time: '19:35' },
          { player: 'Ella Green', school: 'Brunswick', time: '19:40' },
          { player: 'Sofia Martinez', school: 'Frederick', time: '19:45' },
          { player: 'Ava Thompson', school: 'Urbana', time: '19:50' },
          { player: 'Chloe Roberts', school: 'Middletown', time: '20:00' },
          { player: 'Isabella White', school: 'Tuscarora', time: '20:10' },
          { player: 'Lily Baker', school: 'Linganore', time: '20:15' },
          { player: 'Emma Scott', school: 'Oakdale', time: '20:20' }
        ]
      }
    ]
  },
  {
    id: 'golf',
    name: 'Golf',
    standings: [
      {
        name: 'Standings',
        headers: ['Matches'],
        rows: [
          { team: 'Linganore', matches: '15-1' },
          { team: 'Middletown', matches: '14-2' },
          { team: 'Oakdale', matches: '12-4' },
          { team: 'Urbana', matches: '10-6' },
          { team: 'Tuscarora', matches: '8-8' },
          { team: 'Frederick', matches: '6-10' },
          { team: 'Walkersville', matches: '4-12' },
          { team: 'Brunswick', matches: '2-14' }
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Scoring Average (9 Holes)',
        headers: [{ key: 'avg', label: 'Avg' }],
        players: [
          { player: 'Josh Eyler', school: 'Linganore', avg: 36.5 },
          { player: 'Andrew Noble', school: 'Middletown', avg: 37.2 },
          { player: 'Ryan Smith', school: 'Oakdale', avg: 37.8 },
          { player: 'Chris Jones', school: 'Urbana', avg: 38.1 },
          { player: 'Matt Davis', school: 'Linganore', avg: 38.4 },
          { player: 'Tyler Brown', school: 'Tuscarora', avg: 38.9 },
          { player: 'Zach Miller', school: 'Middletown', avg: 39.2 },
          { player: 'Jacob Wilson', school: 'Frederick', avg: 39.5 },
          { player: 'Ben White', school: 'Oakdale', avg: 40.1 },
          { player: 'Sam Taylor', school: 'Walkersville', avg: 40.5 },
          { player: 'Luke Harris', school: 'Urbana', avg: 41.0 },
          { player: 'Ethan Clark', school: 'Linganore', avg: 41.2 },
          { player: 'Noah Robinson', school: 'Brunswick', avg: 42.5 },
          { player: 'Caleb King', school: 'Middletown', avg: 43.0 },
          { player: 'Mason Lee', school: 'Frederick', avg: 44.2 }
        ]
      }
    ]
  }
];