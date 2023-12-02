"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  // $table.empty();
  // loop over board and create the DOM tr/td structure
  const $tableCells = $(".tableCell");

  let currentIndex = 0;

  for (const row in board) {
    for (const letter in row) {

      // Grab specific td to attach to
      const $td = $tableCells.eq(currentIndex);

      // Attach letter to td object
      $td.text(letter)

      // Increment counter
      currentIndex++;
    }
  }

}


start();