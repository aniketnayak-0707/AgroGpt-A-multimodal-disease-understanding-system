import Navbar from "../components/Navbar"
import UploadBox from "../components/UploadBox"
import ResultCard from "../components/ResultCard"

import { useState } from "react"

export default function Home() {

    const [result, setResult] = useState(null)

    return (

        <div className="min-h-screen bg-gradient-to-b from-[#020817] via-[#031127] to-[#041b34] overflow-hidden">

            <Navbar />

            <div className="relative flex flex-col items-center justify-center px-6 py-20">

                <div className="absolute top-32 left-20 w-72 h-72 bg-green-600 opacity-10 blur-[120px] rounded-full"></div>

                <div className="absolute bottom-20 right-20 w-96 h-96 bg-emerald-500 opacity-10 blur-[120px] rounded-full"></div>

                <div className="text-center mb-16 relative z-10">

                    <h1 className="text-7xl font-black text-white tracking-wide drop-shadow-lg">
                        AgroGPT
                    </h1>

                    <p className="text-2xl text-gray-300 mt-6 max-w-3xl leading-10">
                        AI Powered Plant Disease Detection with Explainable AI,
                        Dynamic Disease Knowledge Engine and Intelligent Crop Analysis.
                    </p>

                </div>

                <div className="relative z-10 w-full flex justify-center">
                    <UploadBox setResult={setResult} />
                </div>

                <div className="relative z-10 w-full max-w-7xl mt-16">
                    <ResultCard result={result} />
                </div>

            </div>

        </div>
    )
}