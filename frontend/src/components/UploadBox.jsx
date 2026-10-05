import { useState } from "react"
import axios from "axios"

export default function UploadBox({ setResult }) {

    const [file, setFile] = useState(null)
    const [crop, setCrop] = useState("")
    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {

        if (!file) {

            alert("Please upload an image")
            return
        }

        const formData = new FormData()

        formData.append("file", file)
        formData.append("crop_type", crop)

        try {

            setLoading(true)

            const response = await axios.post(
                "https://ansuman12-agrogpt-backend.hf.space/predict",
                 formData
            )

            setResult(response.data)

        } catch (error) {

            console.log(error)
            alert("Prediction failed")

        } finally {

            setLoading(false)
        }
    }

    return (

        <div className="bg-[#071225] border border-green-900 rounded-3xl p-8 shadow-2xl w-full max-w-2xl backdrop-blur-md">

            <div className="space-y-6">

                <div className="border-2 border-dashed border-green-700 rounded-2xl p-8 text-center hover:border-green-500 transition-all duration-300 bg-[#0b172c]">

                    <input
                        type="file"
                        onChange={(e) => setFile(e.target.files[0])}
                        className="text-white"
                    />

                    <p className="text-gray-400 mt-3 text-sm">
                        Upload crop leaf image for AI analysis
                    </p>

                </div>

                <select
                    value={crop}
                    onChange={(e) => setCrop(e.target.value)}
                    className="w-full bg-[#1e293b] text-white px-5 py-4 rounded-2xl outline-none border border-gray-700"
                >

                    <option value="">
                        Auto Detect Crop
                    </option>

                    <option>
                        Apple
                    </option>

                    <option>
                        Grape
                    </option>

                    <option>
                        Mango
                    </option>

                    <option>
                        Potato
                    </option>

                    <option>
                        Tomato
                    </option>

                    <option>
                        Pepper
                    </option>

                    <option>
                        Maize
                    </option>

                    <option>
                        Rice
                    </option>

                    <option>
                        Cotton
                    </option>

                </select>

                <button
                    onClick={handleSubmit}
                    className="w-full bg-green-600 hover:bg-green-700 transition-all duration-300 py-4 rounded-2xl text-white text-lg font-bold shadow-xl"
                >

                    {
                        loading
                            ? "Analyzing Leaf..."
                            : "Analyze Leaf"
                    }

                </button>

            </div>

        </div>
    )
}