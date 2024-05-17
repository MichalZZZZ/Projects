<?php

namespace App\Controller;

use App\Entity\Photo;
use App\Entity\OpinionSeller;
use App\Entity\User;
use App\Form\UploadPhotoType;
use App\Repository\OpinionSellerRepository;
use App\Repository\UserRepository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Routing\Annotation\Route;


class MyProfileController extends AbstractController
{
    #[Route('delete/avatar', name: 'app_delete_avatar')]
    public function deleteAvatar(EntityManagerInterface $entityManager, Request $request)
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $check = $entityManager->getRepository(Photo::class)->findOneBy(['owner' => $this->getUser()]);

        if($check)
        {
            unlink('img/hosting/'.$check->getFileName());
            $entityManager->remove($check);
            $entityManager->flush();
            $this->addFlash('success', 'Usunięto zdjęcie');
        }

        return $this->redirectToRoute('app_my_profile', ['page' => 1]);
    }

    #[Route('/my/profile/{page}', name: 'app_my_profile')]
    public function index(EntityManagerInterface $entityManager, Request $request, SessionInterface $session, OpinionSellerRepository $opinionSellerRepository, $page): Response
    {
        $this->denyAccessUnlessGranted('ROLE_USER');
        $form = $this->createForm(UploadPhotoType::class);
        $form->handleRequest($request);
        $user = $this->getUser();
        $check = $entityManager->getRepository(Photo::class)->findOneBy(['owner' => $this->getUser()]);

        
        $myOpinion = $entityManager->getRepository(OpinionSeller::class)->findBy(['user'=>$this->getUser()], ['id'=>'DESC']);
        $mean = 0;
        $percent = 0;
        $value = 0;

        foreach ($myOpinion as $opinion)
        {
            $value += $opinion->getScale();
        }

        if ($myOpinion)
        {
            $count = count($myOpinion);
            $mean = round(($value / $count), 2);
            $percent = round(($mean / 5) * 100, 2);
        }

        $paginatorPerPage = OpinionSellerRepository::PAGINATOR_PER_PAGE;
        $offset = ($page - 1) * $paginatorPerPage;
        $commentPaginator = $opinionSellerRepository->getCommentPaginator($user, $offset);
        $totalItems = count($commentPaginator);
        $totalPages = ceil($totalItems / $paginatorPerPage);

        if ($page > $totalPages and $totalPages >= 1)
        {
            $this->addFlash('error', 'Taka strona nie istnieje.');
            return new RedirectResponse($this->generateUrl('index'));
        }

        if ($form->isSubmitted() && $form->isValid())
        {
            if ($this->getUser())
            {
                $pictureFile = $form->get('filename')->getData();
                if ($pictureFile)
                {
                    try
                    {
                        $originalFileName = pathinfo($pictureFile->getClientOriginalName(), PATHINFO_FILENAME);
                        $safeFileName = preg_replace('/[^A-Za-z0-9_]/', '', $originalFileName);
                        $newFileName = $safeFileName .'.'. $pictureFile->guessExtension();

                        if ($check)
                        {
                            $oldFileName = $check->getFilename();
                            unlink('img/hosting/'.$oldFileName);
                            $pictureFile->move('img/hosting', $newFileName);
                            $check->setFilename($newFileName);
                            $entityManager->flush();
                            $this->addFlash('success', 'Zaaktualizowano zdjęcie');
                        }
                        else
                        {
                            $pictureFile->move('img/hosting', $newFileName);
                            $photoEntity = new Photo();
                            $photoEntity->setOwner($this->getUser());
                            $photoEntity->setFilename($newFileName);
                            $entityManager->persist($photoEntity);
                            $entityManager->flush();
                            $this->addFlash('success', 'Dodano zdjęcie');
                        }
                    }
                    catch (\Exception $e)
                    {
                        $this->addFlash('error', 'Nieoczekiwany błąd');
                    }
                }
            }
            else
            {
                $this->addFlash('error', 'Zaloguj się');
            }
        }
        if($check)
        {
            return $this->render('my_profile/index.html.twig', [
                'photoForm' => $form->createView(),
                'latestPhoto' => $check->getFilename(),
                'myOpinion'=> $myOpinion,
                'comments' => $commentPaginator,
                'page' => $page,
                'totalPages' => $totalPages,
                'mean'=>$mean,
                'percent'=>$percent,
            ]);
        }

        return $this->render('my_profile/index.html.twig', [
            'photoForm' => $form->createView(),
            'latestPhoto' => '',
            'myOpinion'=> $myOpinion,
            'comments' => $commentPaginator,
            'page' => $page,
            'totalPages' => $totalPages,
            'mean'=>$mean,
            'percent'=>$percent,
        ]);
    }
}

