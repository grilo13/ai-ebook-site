"use client";

// export const metadata = {
//   title: "Home - Simple",
//   description: "Page description",
// };
import Image from 'next/image'

import {motion} from "framer-motion";
import React, {useEffect, useState} from "react";

import {Banner} from "@/components/banner";
import Footer from "@/components/ui/footer";
import {CheckCircle, XCircle} from "lucide-react";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";

export default function Home() {
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        // Function to update the state based on the window width
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768); // 768px is a common breakpoint for mobile devices
        };

        // Set the initial value
        handleResize();

        // Add event listener
        window.addEventListener("resize", handleResize);

        // Remove event listener on cleanup
        return () => window.removeEventListener("resize", handleResize);
    }, []);
    return (
        <>
            <div className="main-container flex w-screen lg:h-screen items-center justify-center">
                {/*<section className="p-8 h-full flex lg:justify-end items-center w-full">
                    <div className="max-w-[500px]">
                        <div className="py-12">
                            <div className="flex flex-col gap-5">

                                <motion.div
                                    initial={{rotate: 270}}
                                    animate={{rotate: 0}}
                                    transition={{duration: 1, ease: [0.33, 1, 0.68, 1]}}
                                    className="w-10 h-10 bg-[#FF3D00] logo"
                                ></motion.div>
                                <div className="flex gap-2 flex-col">
                                    <Image src="/icon.png" width={300} height={300} alt="Picture of the author"/>
                                    <h1 className="text-xl text-black font-medium">
                                        Generate any book with AI in minutes.
                                    </h1>
                                    <p className="text-base text-black/60">
                                        Discover the power of AI with our E-Book Generator, designed
                                        to turn your curiosity into knowledge. Select any topic, and
                                        our AI instantly compiles a personalized e-book for you.
                                        Ideal for convenient, in-depth learning, our tool simplifies
                                        complex subjects into clear, concise content. Whether you're
                                        a student, professional, or lifelong learner, our AI E-Book
                                        Generator is your go-to resource for digestable, tailored
                                        knowledge.
                                    </p>
                                </div>
                                <div className="flex gap-2">
                                    <a
                                        className="btn btn-orange mb-4 sm:w-auto sm:mb-0"
                                        href="generate-sell"
                                    >
                                        Generate E-Book
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>*/}
                <section className="p-8 h-full flex lg:justify-end items-center w-full">
                    <Card className="max-w-[600px] w-full">
                        <CardHeader>
                            <motion.div
                                initial={{rotate: 270}}
                                animate={{rotate: 0}}
                                transition={{duration: 1, ease: [0.33, 1, 0.68, 1]}}
                                className="w-10 h-10 bg-[#FF3D00] logo mb-4"
                            ></motion.div>
                            <CardTitle className="text-3xl font-bold mb-2">
                                Generate Any Book with AI in Minutes
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <Image src="/icon.png" width={300} height={300} alt="AI E-Book Generator"
                                   className="mx-auto"/>
                            <p className="text-lg text-muted-foreground">
                                Transform your curiosity into knowledge with our AI-powered E-Book Generator.
                                Perfect for students, professionals, and lifelong learners.
                            </p>
                            <ul className="space-y-2">
                                {['Instant, personalized e-books on any topic', 'Simplify complex subjects', 'Tailored, digestible content'].map((feature, index) => (
                                    <li key={index} className="flex items-center space-x-2">
                                        <CheckCircle className="h-5 w-5 text-green-500"/>
                                        <span>{feature}</span>
                                    </li>
                                ))}
                            </ul>
                            <Button size="lg" className="w-full bg-[#FF3D00] hover:bg-[#FF3D00]/90 text-white">
                                <a href="generate-sell" className="text-lg font-semibold">
                                    Generate Your E-Book Now
                                </a>
                            </Button>
                        </CardContent>
                    </Card>
                </section>
                <div
                    className="relative w-full overflow-hidden h-auto border md:border-transparent border-solid border-secondary-black">
                    <Banner/>
                </div>
            </div>
            <Footer/>
        </>
    );
}
