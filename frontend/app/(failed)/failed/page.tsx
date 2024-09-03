'use client'

import Link from 'next/link'
import {XCircle} from "lucide-react"
import {Button} from "@/components/ui/button"

export default function FailedPage() {
    return (
        <section className="min-h-screen flex items-center justify-center bg-gradient-to-b from-red-100 to-white">
            <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
                <div className="space-y-8">
                    <XCircle className="w-20 h-20 text-red-500 mx-auto"/>

                    <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl text-red-700">
                        Oops! Something went wrong
                    </h1>

                    <p className="text-xl text-red-600">
                        We encountered an error while processing your E-book request.
                    </p>

                    <div className="bg-white text-gray-800 rounded-lg p-6 shadow-lg border border-red-200">
                        <h3 className="font-semibold mb-2 text-red-700">What to do next:</h3>
                        <ul className="text-sm list-disc list-inside space-y-2">
                            <li>Please try submitting your request again.</li>
                            <li>If the problem persists, contact our support team for assistance.</li>
                            <li>
                                Email us at{' '}
                                <a href="mailto:nulllabsllc@gmail.com"
                                   className="font-medium text-red-600 hover:underline">
                                    nulllabsllc@gmail.com
                                </a>
                                {' '}with details about your E-book request.
                            </li>
                        </ul>
                    </div>

                    <div className="flex flex-col sm:flex-row justify-center items-center gap-4">
                        <Link href="/generate-sell">
                            <Button
                                variant="outline"
                                className="w-full sm:w-auto bg-white text-red-600 border-red-300 hover:bg-red-50 hover:text-red-700"
                            >
                                Try Again
                            </Button>
                        </Link>
                        <Link href="/">
                            <Button
                                className="w-full sm:w-auto bg-red-500 text-white hover:bg-red-600"
                            >
                                Return to Home
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </section>
    )
}