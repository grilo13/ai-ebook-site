import {Button} from "@/components/ui/button"
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {CheckCircle, MessageCircle, Zap, Clock, Trophy, Globe} from "lucide-react"
import Link from "next/link"

export default function Landing() {
    return (
        <div className="flex flex-col min-h-screen">
            <header className="px-4 lg:px-6 h-14 flex items-center">
                <Link className="flex items-center justify-center" href="#">
                    <Zap className="h-6 w-6 text-blue-600"/>
                    <span className="ml-2 text-2xl font-bold text-gray-900">Fresh News</span>
                </Link>
                <nav className="ml-auto flex gap-4 sm:gap-6">
                    <Link className="text-sm font-medium hover:underline underline-offset-4" href="#features">
                        Features
                    </Link>
                    <Link className="text-sm font-medium hover:underline underline-offset-4" href="#pricing">
                        Pricing
                    </Link>
                    <Link className="text-sm font-medium hover:underline underline-offset-4" href="#about">
                        About
                    </Link>
                </nav>
            </header>
            <main className="flex-1">
                <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-blue-50">
                    <div className="container px-4 md:px-6">
                        <div className="flex flex-col items-center space-y-4 text-center">
                            <div className="space-y-2">
                                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                                    Get Real-Time Football News
                                </h1>
                                <p className="mx-auto max-w-[700px] text-gray-600 md:text-xl">
                                    Join our Telegram group for instant, summarized football updates. Stay ahead of the
                                    game!
                                </p>
                            </div>
                            <div className="space-x-4 mt-6">
                                <Button className="bg-blue-600 text-white" size="lg">
                                    Join Now
                                </Button>
                                <Button variant="outline" size="lg">
                                    Learn More
                                </Button>
                            </div>
                            <div className="grid gap-4 mt-12 sm:grid-cols-2 md:grid-cols-3 text-sm">
                                <div className="flex items-center space-x-2">
                                    <Clock className="w-4 h-4 text-blue-600"/>
                                    <span>24/7 Breaking News</span>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <Trophy className="w-4 h-4 text-blue-600"/>
                                    <span>Exclusive Transfer Insights</span>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <Globe className="w-4 h-4 text-blue-600"/>
                                    <span>Global Football Coverage</span>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <MessageCircle className="w-4 h-4 text-blue-600"/>
                                    <span>Community Discussions</span>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <Zap className="w-4 h-4 text-blue-600"/>
                                    <span>Instant Match Updates</span>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <CheckCircle className="w-4 h-4 text-blue-600"/>
                                    <span>Verified Information</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <section className="w-full py-12 bg-white">
                    <div className="container px-4 md:px-6">
                        <h2 className="text-2xl font-bold text-center mb-8">News Sources</h2>
                        <div className="flex justify-center">
                            <div className="w-full max-w-3xl overflow-hidden">
                                <div className="flex animate-slide">
                                    <div className="flex-none w-1/3 px-4">
                                        <img src="/placeholder.svg?height=60&width=120" alt="A Bola"
                                             className="h-15 object-contain"/>
                                    </div>
                                    <div className="flex-none w-1/3 px-4">
                                        <img src="/placeholder.svg?height=60&width=120" alt="Record"
                                             className="h-15 object-contain"/>
                                    </div>
                                    <div className="flex-none w-1/3 px-4">
                                        <img src="/placeholder.svg?height=60&width=120" alt="O Jogo"
                                             className="h-15 object-contain"/>
                                    </div>
                                    {/* Duplicate set for seamless loop */}
                                    <div className="flex-none w-1/3 px-4">
                                        <img src="/placeholder.svg?height=60&width=120" alt="A Bola"
                                             className="h-15 object-contain"/>
                                    </div>
                                    <div className="flex-none w-1/3 px-4">
                                        <img src="/placeholder.svg?height=60&width=120" alt="Record"
                                             className="h-15 object-contain"/>
                                    </div>
                                    <div className="flex-none w-1/3 px-4">
                                        <img src="/placeholder.svg?height=60&width=120" alt="O Jogo"
                                             className="h-15 object-contain"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <section id="features" className="w-full py-12 md:py-24 lg:py-32">
                    <div className="container px-4 md:px-6">
                        <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12">Why Choose
                            Fresh News?</h2>
                        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
                            <div className="flex flex-col items-center text-center">
                                <Zap className="h-12 w-12 text-blue-600 mb-4"/>
                                <h3 className="text-xl font-bold mb-2">Real-Time Updates</h3>
                                <p className="text-gray-600">Get the latest football news as it happens, no delays.</p>
                            </div>
                            <div className="flex flex-col items-center text-center">
                                <MessageCircle className="h-12 w-12 text-blue-600 mb-4"/>
                                <h3 className="text-xl font-bold mb-2">Concise Summaries</h3>
                                <p className="text-gray-600">Brief, to-the-point news summaries for quick
                                    consumption.</p>
                            </div>
                            <div className="flex flex-col items-center text-center">
                                <CheckCircle className="h-12 w-12 text-blue-600 mb-4"/>
                                <h3 className="text-xl font-bold mb-2">Verified Information</h3>
                                <p className="text-gray-600">All news is fact-checked and verified before sharing.</p>
                            </div>
                        </div>
                    </div>
                </section>
                <section id="pricing" className="w-full py-12 md:py-24 lg:py-32 bg-gray-100">
                    <div className="container px-4 md:px-6">
                        <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12">Choose Your
                            Plan</h2>
                        <div className="grid gap-6 lg:grid-cols-3">
                            <Card>
                                <CardHeader>
                                    <CardTitle>Monthly</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-4xl font-bold mb-2">$9.99</div>
                                    <p className="text-gray-600 mb-4">per month</p>
                                    <Button className="w-full">Subscribe</Button>
                                    <ul className="mt-4 space-y-2">
                                        <li className="flex items-center">
                                            <CheckCircle className="text-green-500 mr-2 h-5 w-5"/>
                                            <span>Real-time updates</span>
                                        </li>
                                        <li className="flex items-center">
                                            <CheckCircle className="text-green-500 mr-2 h-5 w-5"/>
                                            <span>Access to archive</span>
                                        </li>
                                    </ul>
                                </CardContent>
                            </Card>
                            <Card>
                                <CardHeader>
                                    <CardTitle>6 Months</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-4xl font-bold mb-2">$49.99</div>
                                    <p className="text-gray-600 mb-4">$8.33 per month</p>
                                    <Button className="w-full">Subscribe</Button>
                                    <ul className="mt-4 space-y-2">
                                        <li className="flex items-center">
                                            <CheckCircle className="text-green-500 mr-2 h-5 w-5"/>
                                            <span>All Monthly features</span>
                                        </li>
                                        <li className="flex items-center">
                                            <CheckCircle className="text-green-500 mr-2 h-5 w-5"/>
                                            <span>Exclusive content</span>
                                        </li>
                                    </ul>
                                </CardContent>
                            </Card>
                            <Card>
                                <CardHeader>
                                    <CardTitle>Yearly</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="text-4xl font-bold mb-2">$89.99</div>
                                    <p className="text-gray-600 mb-4">$7.50 per month</p>
                                    <Button className="w-full">Subscribe</Button>
                                    <ul className="mt-4 space-y-2">
                                        <li className="flex items-center">
                                            <CheckCircle className="text-green-500 mr-2 h-5 w-5"/>
                                            <span>All 6-month features</span>
                                        </li>
                                        <li className="flex items-center">
                                            <CheckCircle className="text-green-500 mr-2 h-5 w-5"/>
                                            <span>Priority support</span>
                                        </li>
                                    </ul>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </section>
            </main>
            <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
                <p className="text-xs text-gray-500">© 2023 Fresh News. All rights reserved.</p>
                <nav className="sm:ml-auto flex gap-4 sm:gap-6">
                    <Link className="text-xs hover:underline underline-offset-4" href="#">
                        Terms of Service
                    </Link>
                    <Link className="text-xs hover:underline underline-offset-4" href="#">
                        Privacy
                    </Link>
                </nav>
            </footer>
        </div>
    )
}