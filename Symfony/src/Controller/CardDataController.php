<?php

namespace App\Controller;

use App\Form\BlikType;
use App\Form\CardType;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Routing\Annotation\Route;


class CardDataController extends AbstractController
{
    #[Route('/payment/data', name: 'app_card')]
    public function card(Request $request, SessionInterface $session): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $cart = $session->get('cart', []);
        if (empty($cart))
        {
            $this->addFlash('error', 'Koszyk jest pusty.');
            return new RedirectResponse($this->generateUrl('app_cart_show'));
        }

        $form = $this->createForm(CardType::class);
        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid())
        {
            return $this->redirectToRoute('app_cart_save');
        }

        $session = $request->getSession();
        $totalValue= $session->get('totalValue');

        return $this->render('card_data/index.html.twig', [
            'totalValue'=> $totalValue,
            'form'=>$form->createView(),
        ]);
    }

    #[Route('/payment/blik', name: 'app_blik')]
    public function blik(Request $request, SessionInterface $session): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $cart = $session->get('cart', []);

        if (empty($cart))
        {
            $this->addFlash('error', 'Koszyk jest pusty.');
            return new RedirectResponse($this->generateUrl('app_cart_show'));
        }

        $form = $this->createForm(BlikType::class);
        $form->handleRequest($request);
        $session = $request->getSession();
        $totalValue = $session->get('totalValue');

        if ($form->isSubmitted() && $form->isValid())
        {
            return $this->redirectToRoute('app_cart_save');
        }

        return $this->render('blik/index.html.twig', [
            'form' => $form->createView(),
            'totalValue' => $totalValue,
        ]);
    }

}

