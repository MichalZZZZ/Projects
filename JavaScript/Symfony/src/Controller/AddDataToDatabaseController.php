<?php

// src/Controller/AddDataToDatabaseController.php
namespace App\Controller;

use App\Entity\Bugs;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

class AddDataToDatabaseController extends AbstractController
{
    #[Route('/add/data/to/database', name: 'app_add_data_to_database', methods: ['POST'])]
    public function index(Request $request, EntityManagerInterface $entityManager): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        if (!$data) {
            return new JsonResponse(['status' => 'error', 'message' => 'Invalid JSON'], JsonResponse::HTTP_BAD_REQUEST);
        }

        $bug = new Bugs();
        $bug->setDescription($data['description']);
        $bug->setAssignee($data['assignee']);
        $bug->setPriority($data['priority']);
        $bug->setStatus($data['status']);
        $bug->setTimestamp(new \DateTime($data['timestamp']));
        $bug->setUrl($data['url']);
        $bug->setSelector($data['selector']);
        $bug->setUserAgent($data['userAgent']);
        $bug->setPlatform($data['platform']);
        $bug->setScreenResolution($data['screenResolution']);
        $bug->setWindowSize($data['windowSize']);
        $bug->setAttachment($data['attachment'] ?? null);
        $bug->setTypes($data['types'] ?? null);
        $bug->setHidden($data['hidden'] ?? null);

        $entityManager->persist($bug);
        $entityManager->flush();

        return new JsonResponse(['status' => 'success', 'message' => 'Data added successfully'], 200);
    }
}

