function ResultCard({ result }) {

    if (!result) return null

    return (

        <div className="bg-white rounded-[30px] shadow-lg border border-gray-100 overflow-hidden">

            {/* top section */}

            <div className="bg-gradient-to-r from-green-700 to-green-600 p-6 text-white">

                <div className="flex items-center justify-between">

                    <div>

                        <h2 className="text-3xl font-bold capitalize">
                            {result.disease}
                        </h2>

                        <p className="text-green-100 mt-2">
                            AI Disease Detection Result
                        </p>

                    </div>

                    <div className="bg-white/20 px-5 py-3 rounded-2xl text-center">

                        <p className="text-sm">
                            Confidence
                        </p>

                        <h3 className="text-2xl font-bold">
                            {result.confidence}
                        </h3>

                    </div>

                </div>

            </div>

            {/* content */}

            <div className="p-8">

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                    {/* left section */}

                    <div>

                        <div className="mb-8">

                            <h3 className="text-2xl font-bold text-green-900 mb-3">
                                Description
                            </h3>

                            <p className="text-gray-600 leading-8">
                                {result.description}
                            </p>

                        </div>

                        <div className="mb-8">

                            <h3 className="text-2xl font-bold text-green-900 mb-3">
                                Cause
                            </h3>

                            <p className="text-gray-600 leading-8">
                                {result.cause}
                            </p>

                        </div>

                    </div>

                    {/* right section */}

                    <div>

                        <div className="mb-8">

                            <h3 className="text-2xl font-bold text-green-900 mb-3">
                                Remedy
                            </h3>

                            <p className="text-gray-600 leading-8">
                                {result.remedy}
                            </p>

                        </div>

                        <div className="mb-8">

                            <h3 className="text-2xl font-bold text-green-900 mb-3">
                                Prevention
                            </h3>

                            <p className="text-gray-600 leading-8">
                                {result.prevention}
                            </p>

                        </div>

                    </div>

                </div>

                {/* gradcam */}

                <div className="mt-10">

                    <h3 className="text-2xl font-bold text-green-900 mb-5">
                        Explainable AI Visualization
                    </h3>

                    <div className="rounded-[30px] overflow-hidden border border-gray-200">

                        <img
                            src={`https://ansuman12-agrogpt-backend.hf.space${result.gradcam}?t=${Date.now()}`}
                            alt="gradcam"
                            className="w-full object-cover"
                        />

                    </div>

                </div>

            </div>

        </div>

    )
}

export default ResultCard