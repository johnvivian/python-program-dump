import pyttsx
engine = pyttsx.init()
engine.setProperty('rate', 150)
engine.setProperty('pitch', 0)
voices = engine.getProperty('voices')
engine.say("Hello") 
def onStart(name):
   print 'starting', name
def onWord(name, location, length):
   print 'word', name, location, length
def onEnd(name, completed):
   print 'finishing', name, completed
   if name == 'fox':
      engine.say('What a lazy dog!', 'dog')
   
    


for voice in voices:
   engine.setProperty('voice', voice.id)
   engine = pyttsx.init()
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
engine.startLoop()
engine.runAndWait()