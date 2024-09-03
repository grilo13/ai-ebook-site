'use client'

import Link from 'next/link'
import { CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function SuccessPage() {
  return (
    <section className="min-h-screen flex items-center justify-center bg-gradient-to-b from-green-100 to-white">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
        <div className="space-y-8">
          <CheckCircle className="w-20 h-20 text-green-500 mx-auto" />

          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl text-black-700">
            Success! Your E-book is on its way
          </h1>

          <p className="text-xl text-green-600">
            The E-book will be sent to your email in less than 10 minutes.
          </p>

          <div className="bg-white text-gray-800 rounded-lg p-6 shadow-lg border border-green-200">
            <h3 className="font-semibold mb-2 text-black-700">Important Note:</h3>
            <p className="text-sm">
              In the rare case of a platform error, if you do not receive your E-book within 1 day,
              please email <span className="font-medium text-green-600">nulllabsllc@gmail.com</span> with the topic
              and target audience of the book. Don't forget to check your spam folder!
            </p>
          </div>

          <div className="flex flex-col sm:flex-row justify-center items-center gap-3">
            <Link href="/generate-sell">
              <Button
                  variant="outline"
                  className="w-full sm:w-auto bg-white text-black-600 border-green-300 hover:bg-green-50 hover:text-green-700"
              >
                Generate More E-books
              </Button>
            </Link>
            <Link href="/">
              <Button
                  className="w-full sm:w-auto bg-green-500 text-white hover:bg-green-600"
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