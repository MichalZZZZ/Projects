<?php

namespace App\Form;

use App\Entity\User;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\PasswordType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class PasswordUpdateForm extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('oldPassword', PasswordType::class, [
                'label' => 'Stare hasło',
                'mapped' => false,
            ])
            ->add('password', PasswordType::class, [
                'label' => 'Nowe hasło',
                'mapped' => true,
            ])
            ->add('confirmPassword', PasswordType::class, [
                'label' => 'Powtórz hasło',
                'mapped' => false,
            ]);
    }

    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults([
            'data_class' => User::class,
        ]);
    }
}
