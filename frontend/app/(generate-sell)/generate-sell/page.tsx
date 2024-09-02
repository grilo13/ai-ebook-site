"use client";

import React, {useState} from "react";

import {sendPreviewPostRequest} from "./preview";
import {sendCheckoutPostRequest} from "./checkout";
import {FacebookPixel} from "@/components/facebook/pixel";
import Footer from "@/components/ui/footer";
import {Label} from '@/components/ui/label';
import {RadioGroup, RadioGroupItem} from '@/components/ui/radio-group';


interface PreviewResponse {
    id: string;
}

interface StatusResponse {
    status: string;
}

interface PdfResponse {
    file_url: string;
}

export default function Generate() {
    const [input1, setInput1] = useState<string>("");
    const [input2, setInput2] = useState<string>("");
    const [tier, setTier] = useState('basic');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [pdfUrl, setPdfUrl] = useState<string | null>(null);

    const tiers = [
        {
            id: 'basic',
            name: 'Basic',
            price: '$0.99',
            features: ['40-50 pages', '5 chapters', '3 subsections per chapter'],
        },
        {
            id: 'premium',
            name: 'Premium',
            price: '$1.49',
            features: [
                '50-60 pages',
                '7 chapters',
                '4 subsections per chapter',
                'Enhanced AI writing',
            ],
        },
        {
            id: 'topPremium',
            name: 'Top Premium',
            price: '$1.99',
            features: [
                '60-70 pages',
                '10 chapters',
                '5 subsections per chapter',
                'Advanced AI writing',
                'Custom cover design',
            ],
        },
    ]

    // Use environment variable for the API URL
    const apiUrl: string =
        process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

    // Use environment variable for the API URL
    const frontendUrl: string =
        process.env.NEXT_PUBLIC_FRONTEND_URL ?? "http://127.0.0.1:3000";

    const tocUrl: string = frontendUrl + "/toc"

    const handleCheckoutButtonClick = () => {
        sendCheckoutPostRequest(input1, input2, tier)
            .then((redirect_url) => {
                console.log(redirect_url);
                window.location.href = redirect_url; // Handle a successful response if needed.
            })
            .catch((error) => {
                console.error(error); // Handle errors if the request fails.
            });
    };

    const handlePreviewButtonClick = () => {
        console.log("handlePreviewButtonClick!");
        setIsLoading(true);
        sendPreviewPostRequest(input1, input2)
            .then((response: PreviewResponse) => {
                const bookId = response.id;
                console.log(bookId);
                pollForStatus(bookId);
            })
            .catch((error: Error) => {
                console.error(error);
                setIsLoading(false);
            });
    };

    const pollForStatus = (bookId: string): void => {
        console.log("Polling!");
        setTimeout(() => {
            fetch(`${apiUrl}/check_ebook_status/${bookId}`)
                .then((response) => response.json())
                .then((data: StatusResponse) => {
                    console.log("data", data);
                    console.log("data status", data.status);
                    if (data.status === "completed") {
                        getPDF(bookId);
                    } else {
                        pollForStatus(bookId); // Continue polling
                    }
                });
        }, 1000); // Poll every  secondsapi/check_status
    };

    const getPDF = (bookId: string): void => {
        fetch(`${apiUrl}/get_pdf/${bookId}`)
            .then((response) => response.json())
            .then((data: PdfResponse) => {
                console.log("before inserting the url", data.file_url);
                setPdfUrl(data.file_url);
                setIsLoading(false);
                console.log("pdf url", pdfUrl);
                console.log("set is loading", isLoading);
            });
    };

    const resetPreview = (): void => {
        setPdfUrl(null);
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>): void => {
        if (e.key === "Enter" && input1 && input2) {
            handlePreviewButtonClick();
        }
    };

    return (
        <>
            <FacebookPixel/>
            <noscript>
                <img height="1" width="1" style={{display: 'none'}}
                     src="https://www.facebook.com/tr?id=1429806270964834&ev=PageView&noscript=1"/>
            </noscript>
            <section className="main-container flex w-screen h-screen overflow-auto">
                <div className="w-full flex md:justify-end items-center px-8 py-12">
                    <div className="max-w-[500px] w-full flex flex-col">
                        {/* Page header */}
                        <div className="flex gap-2 flex-col mb-4">
                            <h1 className="text-xl text-black font-medium">
                                Create Your E-Book
                            </h1>
                            <p className="text-base text-black/60">
                                Start by specifying the topic of your desired e-book,
                                anything from global history to modern technology. Then, define
                                your target audience — that's who you will sell to.Our AI uses this information to
                                customize content making the reading experience uniquely engaging and relevant. Finally,
                                click
                                'Generate E-book' to start the process!
                            </p>
                        </div>

                        {/* Form */}
                        <div className="w-full">
                            <div className="flex flex-wrap -mx-3 mb-4">
                                <div className="w-full px-3">
                                    <label className="block text-gray-800 text-sm font-medium mb-1">
                                        Topic
                                    </label>
                                    <input
                                        id="topic"
                                        type="text"
                                        value={input1}
                                        onChange={(e) => setInput1(e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        className="form-input w-full text-gray-800 bg-stone-50 rounded-md border-primary-black"
                                        placeholder="How To Lose Stubborn Body Fat"
                                        required
                                        disabled={isLoading}
                                        maxLength={100}
                                    />
                                </div>
                            </div>
                            <div className="flex flex-wrap -mx-3 mb-4">
                                <div className="w-full px-3">
                                    <div className="flex justify-between">
                                        <label className="block text-gray-800 text-sm font-medium mb-1">
                                            Target Audience
                                        </label>
                                    </div>
                                    <input
                                        id="target_audience"
                                        type="text"
                                        value={input2}
                                        onChange={(e) => setInput2(e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        className="form-input w-full text-gray-800"
                                        placeholder="Ex. Middle Aged Moms"
                                        required
                                        disabled={isLoading}
                                        maxLength={100}
                                    />
                                </div>
                            </div>
                            <div className="flex flex-wrap -mx-3 mt-6">
                                <div className="w-full px-3">
                                    {pdfUrl ?
                                        <div className="flex justify-between flex-col">
                                            <button
                                                className={"btn btn-blue w-full"}
                                                onClick={
                                                    pdfUrl
                                                        ? handleCheckoutButtonClick
                                                        : handlePreviewButtonClick
                                                }
                                                disabled={isLoading}
                                            >Purchase E-Book
                                            </button>
                                            <div className="flex flex-wrap mt-6">
                                                <div>
                                                    <Label>Generation Tier</Label>
                                                    <RadioGroup value={tier} onValueChange={setTier}
                                                                className="grid gap-4 mt-2">
                                                        {tiers.map((t) => (
                                                            <div key={t.id} className="flex items-center space-x-2">
                                                                <RadioGroupItem value={t.id} id={t.id}/>
                                                                <Label htmlFor={t.id} className="flex flex-col">
                                                                    <span
                                                                        className="font-semibold">{t.name} - {t.price}</span>
                                                                    <span
                                                                        className="text-sm text-muted-foreground">{t.features.join(', ')}</span>
                                                                </Label>
                                                            </div>
                                                        ))}
                                                    </RadioGroup>
                                                </div>
                                            </div>
                                        </div>
                                        : <button
                                            className={
                                                pdfUrl ? "btn btn-blue w-full" : "btn btn-orange w-full"
                                            }
                                            onClick={
                                                pdfUrl
                                                    ? handleCheckoutButtonClick
                                                    : handlePreviewButtonClick
                                            }
                                            disabled={isLoading}
                                        >Generate E-Book
                                        </button>
                                    }
                                    {/*<p className="mt-2 text-sm text-gray-600">
                                        *E-Book length will be 40-50 pages. It will consist of 5 chapters, each having 3
                                        subsections, as outlined in the previewed Table of Contents.
                                    </p>*/}
                                    <p className="mt-4 text-sm text-gray-600">
                                        *Final E-Book may differ slightly than preview, as it will be regenerated.
                                    </p>
                                    {pdfUrl && (
                                        <div className="">
                                            <p className="mt-2 text-sm text-gray-600">
                                                *By purchasing this e-book, you are agreeing to the
                                                <a href={tocUrl} className="text-blue-600 hover:underline"> Terms and
                                                    Conditions</a> of the website.
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                {/* PDF preview */}

                <div
                    className="m-4 rounded-md md:w-full flex justify-center items-center bg-white/50 px-8 py-12 overflow-hidden">
                    {/* Page header */}
                    {isLoading ? (
                        <div className="max-w-[500px] flex flex-col">
                            <div className="max-w-[500px] flex flex-col">
                                {/* Page header */}
                                <div className="flex flex-col mb-4 items-center">
                                    <h1 className=" text-black font-medium text-center">
                                        Preview is loading. It will appear in around a minute!
                                    </h1>
                                    <button className="text-sm" onClick={handleCheckoutButtonClick}>
                                        Don't want to wait? Click{" "}
                                        <span className="font-medium underline text-[#FF3D00]">
                      here
                    </span>{" "}
                                        to continue to purchase!
                                    </button>
                                    <p
                                        className={`text-4xl flex h-full justify-center items-center`}
                                    >
                    <span className="animate-[bounce_1s_ease-in-out_infinite]">
                      .
                    </span>
                                        <span className="animate-[bounce_1s_ease-in-out_.1s_infinite]">
                      .
                    </span>
                                        <span className="animate-[bounce_1s_ease-in-out_.2s_infinite]">
                      .
                    </span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    ) : pdfUrl ? (
                        <iframe src={`${pdfUrl}`} className='w-full h-auto min-h-screen rounded-md shadow-2xl'/>
                    ) : (
                        <div className="max-w-[500px] flex flex-col">
                            <div className="flex gap-2 flex-col mb-4 items-center">
                                <h1 className="text-black/40 font-medium uppercase text-sm tracking-wide text-center">
                                    A preview will appear here upon generation...
                                </h1>
                            </div>
                        </div>
                    )}
                </div>
            </section>
            <Footer/>
        </>
    );
}
