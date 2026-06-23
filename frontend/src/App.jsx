import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'

function App() {
  const [query, setQuery] = useState("")
  const [loading, setLoading] = useState(false)
  const [agentSteps, setAgentSteps] = useState([])
  const [report, setReport] = useState("")

  const handleResearch = () => {
    if (!query.trim()) {
      alert("please enter a research question")
      return
    }
    console.log(query)
    setLoading(true)
    setAgentSteps([])
    setReport("")

    const eventSource = new EventSource(`http://localhost:8000/research?query=${encodeURIComponent(query)}`)

    console.log("EventSource created:", eventSource.url)   


    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.node === "report") {
        setReport(data.data.final_report)
        setLoading(false)
        eventSource.close()
      }
      else {
        setAgentSteps(prev => [...prev, data])
      }
    }

    eventSource.onerror = (error) => {
      console.log("EventSource error:", error)
      setLoading(false)
      eventSource.close()
    }

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
          {loading ? "Researching...." : "Start Research"}
        </button>
        {agentSteps.length > 0 && (
          <div className="mt-8 space-y-3">
            <h2 className="text-xl font-semibold text-gray-300">Agent Progress</h2>
            {agentSteps.map((step, index) => (
              <div key={index} className="bg-gray-800 rounded-lg p-4 border-l-4 border-blue-500">
                <div className="flex items-center gap-2">
                  <span className="text-green-400 font-bold">✓</span>
                  <span className="text-blue-400 font-semibold capitalize">
                    {step.node}
                  </span>
                  <span className="text-gray-400 text-sm">completed</span>
                </div>
                {step.node === "planner" && (
                  <ul className="mt-2 ml-6 text-gray-300 text-sm space-y-1">
                    {step.data.sub_questions?.map((q, i) => (
                      <li key={i}>• {q}</li>
                    ))}
                  </ul>
                )}
                {step.node === "critic" && (
                  <p className="mt-2 ml-6 text-gray-300 text-sm">
                    {step.data.critique}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}

        {report && (
          <div className="mt-8 bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-300 mb-4">
              Final Report
            </h2>
            <pre className="text-gray-200 text-sm whitespace-pre-wrap leading-relaxed">
              {report}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
