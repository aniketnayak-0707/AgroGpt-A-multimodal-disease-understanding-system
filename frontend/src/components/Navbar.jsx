export default function Navbar() {

    return (

        <div className="w-full flex items-center justify-between px-8 py-5 bg-white shadow-md">

            <div>

                <h1 className="text-5xl font-black text-green-700 tracking-wide">
                    AGRO-GPT
                </h1>

                <p className="text-green-600 mt-1 text-sm">
                    AI-powered Plant Disease Detection
                </p>

            </div>

            <button className="bg-green-700 hover:bg-green-800 text-white px-6 py-3 rounded-2xl transition-all duration-300 shadow-lg">
                About Project
            </button>

        </div>
    )
}