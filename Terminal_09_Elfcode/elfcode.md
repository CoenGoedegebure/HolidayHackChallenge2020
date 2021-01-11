Level 1
```
elf.moveLeft(10)
elf.moveUp(10)
```

Level 2
```
elf.moveLeft(6)
elf.pull_lever(elf.get_lever(0) + 2)
elf.moveLeft(4)
elf.moveUp(10)
```

Level 3
```
for (var i = 0; i < 3; i++)
   elf.moveTo(lollipop[i])
elf.moveUp(1)
```

Level 4
```
for (var i = 0; i < 3; i++) {
  elf.moveLeft(3)
  elf.moveUp(11)
  elf.moveLeft(3)
  elf.moveDown(11)
}
```

Level 5
```
elf.moveTo(lollipop[1])
elf.moveTo(lollipop[0])
elf.tell_munch(elf.ask_munch(0).filter(e => Number.isInteger(e)))
elf.moveUp(2)
```

Level 6
```
for (var i = 0; i < 4; i++)
  elf.moveTo(lollipop[i])

elf.moveLeft(8)
elf.moveUp(2)
json = elf.ask_munch(0)
elf.tell_munch(Object.keys(json).find(key => json[key] === 'lollipop'))
elf.moveUp(2)
```

Level 7 (Bonus)
```
function munchy(input) {
  var sum = 0;
  input.flat().forEach(a => sum += Number.isInteger(a) ? a : 0)
  return sum;
}

var moves = [elf.moveDown, elf.moveLeft, elf.moveUp, elf.moveRight]

for (var i = 0; i < 7; i++) {
  moves[i % 4](i + 1)
  elf.pull_lever(i)
}

elf.moveRight(8)
elf.moveUp(2)
elf.moveLeft(4)
elf.tell_munch(munchy)
elf.moveUp(2)
```

Level 8 (Bonus)
```
function munchy(input) {
  for (var record = 0; record < input.length; record++) {
    var key = Object.keys(input[record]).find(b => input[record][b] === 'lollipop');
    if (key !== undefined) {
      return key;
    }
  }
}

var moves = [elf.moveRight, elf.moveLeft]
var sum_levers = 0
for (var i = 0; i < 6; i++) {
  moves[i % 2](i * 2 + 1)
  sum_levers += elf.get_lever(i)
  elf.pull_lever(sum_levers)
  elf.moveUp(2)
}
elf.tell_munch(munchy)
elf.moveRight(12)
```