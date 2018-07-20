var pos = require('pos');
var words = new pos.Lexer().lex("Alan Smith, a prolific movie director, has over 50 movies to his name, although he is considered one of the worst directors of all time.");
var tagger = new pos.Tagger();
var taggedWords = tagger.tag(words);
for (i in taggedWords) {
    var taggedWord = taggedWords[i];
    var word = taggedWord[0];
    var tag = taggedWord[1];
    console.log(word + " /" + tag);
}

// // extend the lexicon
// tagger.extendLexicon({'Obama': ['NNP']});
// tagger.tag(['Mr', 'Obama']);