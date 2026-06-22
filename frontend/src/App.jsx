import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'

function App() {
  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [agentSteps, setAgentSteps] = useState([])
  const [report, setReport]=useState("")

  const handleResearch = () => {
    if (!query.trim()) return
    setLoading(true)
    setAgentSteps([])
    setReport("")
  }

  const eventSource=new EventSource(`http://localhost:8000/research?query=${encodeURIComponent(query)}`)

  eventSource.onmessage=(event)=>{
    const data=JSON.parse(event.data)
    if(data.node==="report") {
      setReport(data.data.final_report)
      setLoading(false)
      eventSource.close()
    }
    else {
      setAgentSteps(prev=>[...prev,data])
    }
  }

  eventSource.onerror = () => {
    setLoading(false)
    eventSource.close()
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <h1 className="text-3xl font-bold text-center mb-8">
        Research Assistant
      </h1>
      <div className="max-w-2xl mx-auto">
        <textarea
          className="w-full bg-gray-800 text-white rounded-lg p-4 h-32 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter your research question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={handleResearch}
          disabled={loading}
          className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 rounded-lg transition-colors"

        >
          {loading?"Researching....":"Start Research"}
        </button>
      </div>
    </div>
  )
}

export default App
