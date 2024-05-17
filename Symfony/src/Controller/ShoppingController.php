<?php

namespace App\Controller;

use App\Entity\Car;
use App\Entity\SpecialOffert;
use App\Entity\Transaction;
use App\Entity\User;
use App\Form\SpecialOffertType;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Routing\Annotation\Route;

class ShoppingController extends AbstractController
{
    #[Route('/cart/add/one/{id}', name: 'app_cart_add')]
    public function addToCart(Request $request, EntityManagerInterface $entityManager, SessionInterface $session, $id)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $cart = $session->get('cart', []);
        $car = $entityManager->getRepository(Car::class)->find($id);

        if (!$car)
        {
            $this->addFlash('error', 'Produkt o podanym identyfikatorze nie został znaleziony.');
            return new RedirectResponse($this->generateUrl('index'));
        }

        $quantity = $car->getQuantity();
        $myCar = $car->getOwner();
        $user = $this->getUser();

        if ($user)
        {
            if ($user == $myCar)
            {
                return new JsonResponse(['message' => 'Nie można dodać swojego produktu!'], 400);
            }
            else
            {
                $cart[$id] = isset($cart[$id]) ? $cart[$id] + 1 : 1;
                if ($cart[$id] > 1)
                {
                    $response = ['success' => false, 'message' => 'Produkt jest już w koszyku!'];
                    return new JsonResponse($response);
                }
                else
                {
                    if ($quantity > 0)
                    {
                        $session->set('cart', $cart);
                        $response = ['success' => true, 'message' => 'Produkt został dodany do koszyka!'];
                        return new JsonResponse($response);
                    }
                    else
                    {
                        $response = ['error' => true, 'message' => 'Brak danego produktu.'];
                        return new JsonResponse($response);
                    }
                }
            }
        }
        else
        {
            $this->addFlash('error', 'Prosze się zalogować.');
            return new RedirectResponse($this->generateUrl('index'));
        }
    }

    #[Route('/cart/add/{id}', name: 'app_cart_add_count')]
    public function addToCartCount(Request $request, EntityManagerInterface $entityManager, SessionInterface $session, $id)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $car = $entityManager->getRepository(Car::class)->find($id);
        $count = $request->get('quantity');
        $cart = $session->get('cart', []);

        if (!$car)
        {
            $this->addFlash('error', 'Nie znaleziono wybranego produktu.');
            return $this->redirectToRoute('app_cart_show');
        }
        if ($count > $car->getQuantity())
        {
            $this->addFlash('error', 'Za duża ilość wybranego produktu!');
        }
        else
        {
            $cart[$id] = $count;
            $session->set('cart', $cart);
        }

        return $this->redirectToRoute('app_cart_show');
    }

    #[Route('/cart/remove/position/{id}', name: 'app_cart_remove_position')]
    public function removePositionFromCart(Request $request, SessionInterface $session, $id)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $cart = $session->get('cart', []);

        if (!isset($cart[$id]))
        {
            $this->addFlash('error', 'Nie znaleziono pozycji w poszyku.');
            return new RedirectResponse($this->generateUrl('index'));
        }

        unset($cart[$id]);
        $session->set('cart', $cart);
        $response = ['success' => true, 'message' => 'Usunięto pozycję z koszyka.'];
        return new JsonResponse($response);
    }

    #[Route('/cart', name: 'app_cart_show')]
    public function showCart(Request $request, SessionInterface $session, EntityManagerInterface $entityManager)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $session = $request->getSession();
        $cart = $session->get('cart', []);
        $totalValue = 0;
        $products = [];

        foreach ($cart as $id => $quantity)
        {
            $product = $entityManager->getRepository(Car::class)->find($id);

            if ($product)
            {
                $price = $product->getPrice();
                $subtotal = $price * $quantity;
                $totalValue += $subtotal;
                $products[] = [
                    'product' => $product,
                    'quantity' => $quantity,
                    'imageUrl' => $product->getPhotopath(),
                    'positionQuantity' => $product->getQuantity(),
                ];
            }
        }

        $form = $this->createForm(SpecialOffertType::class);
        $form->handleRequest($request);
        $saving = 0;
        $firstTotalValue = $totalValue;

        if ($form->isSubmitted() && $form->isValid())
        {
            $code = $form->get('code')->getData();

            if ($code)
            {
                $codeTwo = $entityManager->getRepository(SpecialOffert::class)->findOneBy(['code' => $code]);

                if ($codeTwo)
                {
                    $value = $codeTwo->getValue();
                    $totalValue = $totalValue * (1 - $value);
                    $saving = $firstTotalValue - $totalValue;
                    $this->addFlash('success', 'Kod zrealizowany!');
                }
                else
                {
                    $this->addFlash('error', 'Nie znaleziono kodu.');
                }
            }
        }

        $session->set('totalValue', $totalValue);
        $count = count($products);

        return $this->render('shopping/index.html.twig', [
            'cart' => $products,
            'totalValue'=> $totalValue,
            'count'=> $count,
            'form' => $form->createView(),
            'firstTotalValue'=>$firstTotalValue,
            'saving'=>$saving,
        ]);
    }

    #[Route('/cart/clear', name: 'app_cart_clear')]
    public function clearCart(SessionInterface $session)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $cart = $session->get('cart', []);

        if (empty($cart))
        {
            $this->addFlash('error', 'Koszyk jest pusty.');
            return new RedirectResponse($this->generateUrl('app_cart_show'));
        }

        $session->remove('cart');
        $response = ['success' => true, 'message' => 'Koszyk został wyczyszczony'];
        return new JsonResponse($response);
    }

    #[Route('/cart/save', name: 'app_cart_save')]
    public function saveCartToDatabase(EntityManagerInterface $entityManager, Request $request)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $session = $request->getSession();
        $cart = $session->get('cart', []);

        if (empty($cart))
        {
            $this->addFlash('error', 'Koszyk jest pusty.');
            return new RedirectResponse($this->generateUrl('app_cart_show'));
        }
        if ($cart)
        {
            $user = $this->getUser();

            foreach ($cart as $id => $quantity)
            {
                $product = $entityManager->getRepository(Car::class)->find($id);
                $owner = $product->getOwner()->getId();
                $userSeller = $entityManager->getRepository(User::class)->find($owner);

                if ($product)
                {
                    $purchase = new Transaction();
                    $purchase->setProduct($product->getName().' '. $product->getModel());
                    $purchase->setQuantity($quantity);
                    $purchase->setPrice($product->getPrice());
                    $purchase->setPhotoPath($product->getPhotoPath());
                    $purchase->setCreationDate(new \DateTime());
                    $purchase->setUser($user);
                    $purchase->setUserlogin($user->getUsername());
                    $purchase->setUseremail($user->getEmail());
                    $purchase->setUsername($user->getName());
                    $purchase->setUserlastname($user->getLastname());
                    $purchase->setUserphone($user->getPhone());
                    $purchase->setSellerlogin($userSeller->getUsername());
                    $purchase->setSelleremail($userSeller->getEmail());
                    $purchase->setSellername($userSeller->getName());
                    $purchase->setSellerlastname($userSeller->getLastname());
                    $purchase->setSellerphone($userSeller->getPhone());
                    $purchase->setSellerId($owner);
                    $x = $product->getQuantity() - $quantity;
                    $product->setQuantity($x);
                    $entityManager->persist($purchase);
                }
            }

            $session = $request->getSession();
            $session->remove('cart');
            $entityManager->flush();
            $this->addFlash('success', 'Dziękujemy za zakup przedmiotów w naszym sklepie.');
        }

        return $this->redirectToRoute('app_cart_show');
    }
}

