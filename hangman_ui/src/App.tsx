import { useEffect, useState } from 'react'
import api from './api'
import './App.css'

function App() {

  const [userGuess, setUserGuess] = useState<string>("")
  const [message,setMessage] = useState<string>("")
  const [additionalMessage,setAdditionalMessage] = useState<string>("")
  const [guessedLetters,setGuessedLetters] = useState<string[]>([])
  const [showLetters,setShowLetters]  = useState<string[]>([])
  const [lives,setLives] = useState<number>(6)
  const [gameOver,setGameOver] = useState<boolean>(false)
  const [wordLength,setWordLength] = useState<number>(0)
  const [error,setError] = useState<string|null>("")
  
  useEffect(()=>{
    const Display = async () =>{
    setError(null)
    try{

      await api.post("/reset")

      const response = await api.get("/word-length")
      setWordLength(response.data.Length)
    }catch(error:any){
      setError("Error: Coudlnt get word length")
    }
  }
    Display()
  },[])


  const NewGame = async (e:React.MouseEvent<HTMLButtonElement>) => {
    setError(null)
    try {
      await api.post("/reset")
      setGuessedLetters([])
      setShowLetters([])
      setLives(6)
      setMessage("")
      setUserGuess("")
      setGameOver(false)
      setAdditionalMessage("")

      const response = await api.get("/word-length")
      setWordLength(response.data.Length)
    }catch(error:any){
      console.error(error)
      setError("Error: Couldnt create a new game")
    }
  }

  const HandleSubmit = async (e:React.KeyboardEvent<HTMLInputElement>) =>{
    if(lives===0) return;
    if(e.key !== "Enter") return;
    e.preventDefault()
    setError(null)
    try{
      const response = await api.post("/check-letter",{guess:userGuess})
      if(response.status === 200){
        setMessage(response.data.Message)
        setGuessedLetters(response.data.Guessed)
        setShowLetters(response.data.Display)
        setLives(response.data.Lives)
        setGameOver(response.data.Game_Over)
        setAdditionalMessage(response.data.Additional_Message)
      }
    }catch(error:any){
      console.error("Error: ",error)
      if(error.response){
        setError(error.response.data.detail)
      }else{
        setError("Error: Couldnt process letter check")
      }
    }
    setUserGuess("")
  }
  return (
    <div className='bg-orange-100 min-h-screen min-w-screen'>
      <div className='mx-5 pt-5 text-red-600 font-bold text-6xl'>
        <h1 className='border w-75 mx-auto bg-orange-200 pl-3 pb-3 rounded-md'>Hangman</h1>
      </div>
      <div className='border rounded-md mx-10 mt-10 text-red-600 font-bold bg-orange-200 text-center'>
        <h1 className='text-3xl pt-1'>Rules of the game:</h1>
        <p className='text-xl'>You have to find the word by guessing in letters</p>
        <p className='text-xl pb-2'>Each wrong guess takes away a life</p>
      </div>
      <div className='border rounded-md mx-10 mt-10 text-red-600 font-bold flex justify-center bg-orange-200 h-40'>
        {showLetters.length>0 ?
        showLetters.map((letter,i)=>(
          <div key={i} className='mr-2 text-9xl'>
            <p>{letter}</p>
          </div>
        ))
        :Array.from({length:wordLength}).map((_,i) => (
          <div key={i} className='mr-2 text-9xl'>
            <p>_</p>
          </div>
        ))}
      </div>
      <div className='border rounded-md flex justify-between mx-10 mt-10 text-red-600 font-bold bg-orange-200 pl-5 pt-2'>
        <div className='w-full text-xl'>
          <label>Enter Letter: </label>
          <input className='border-red-300 outline-none border-3 pl-2 w-10'  maxLength={1} minLength={1} type="text" value={userGuess} onChange={(e) => setUserGuess(e.target.value)} onKeyDown={HandleSubmit}/>
          <p>Lives: {lives}</p>
        </div>
        <div className='text-center w-full text-xl'>
          <p>{gameOver === true? 
            <div>
              <p>{additionalMessage}</p>  
              <button type="submit" className='text-black border-3 rounded-md bg-yellow-200 mt-2 mb-4 cursor-pointer' onClick={NewGame}>Play Again</button>
            </div> 
            : message||""}</p>
          <p className={`${error ? "border-red-300 outline-none border-3 mb-2":"" }`}>{error||""}</p>
        </div>
        <div className='w-full text-center text-xl'>
          <p>Letters Guessed: {guessedLetters.join(",")||""}</p>
      </div>
      </div>
    </div>
  )
}

export default App
