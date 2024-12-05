import fs from "fs";
import readline from "readline";

const rl = readline.createInterface({
  input: fs.createReadStream("input.txt"),
  crlfDelay: Infinity,
});

let result = 0
let letters = [] // Move initialization here

rl.on("line", (line) => {
  letters.push(line.split(''))
});

rl.on("close", () => {
  console.log(letters.length, letters[0].length)

  for(let i = 0; i < letters.length; i++) { 
    for(let j = 0; j < letters[i].length; j++) {  
      if(letters[i][j] === 'X'){
        let res =
          //right
          findRestOfWord(letters, i+1, j, [1, 0], 'X')
          //left
          + findRestOfWord(letters, i-1, j, [-1, 0], 'X')
          // top right
          + findRestOfWord(letters, i+1, j+1, [1, 1], 'X') 
          // top left
          + findRestOfWord(letters, i+1, j-1, [1, -1], 'X') 
          // bottom left
          + findRestOfWord(letters, i-1, j-1, [-1, -1], 'X') 
          // bottom right
          + findRestOfWord(letters, i-1, j+1, [-1, 1], 'X') 
          // top
          + findRestOfWord(letters, i, j+1, [0, 1], 'X')
          // bottom
          + findRestOfWord(letters, i, j-1, [0, -1], 'X')
        result += res 
      }
    }
  }
  console.log(result)
});

function findRestOfWord(letters, i, j, dir, oldWord) {
    
    if (oldWord.length === 4) {
      return (oldWord === "XMAS") ? 1 : 0
    }
    if(i >= letters.length || j >= letters[0].length || j < 0 || i < 0) {
      return 0
    }
    const word = oldWord + letters[i][j]
    return findRestOfWord(letters, i+dir[0], j+dir[1], dir, word)
} 